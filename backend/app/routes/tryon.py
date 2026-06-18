import os
import uuid
import requests
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from app.services.piapi_service import PiAPIService
from app.services.prompt_builder import build_prompt_with_context, build_apparel_prompt_with_context
from app.services.catalog_service import get_catalog_service
from app.utils.file_handler import FileHandler
from app.services.gemini_service import GeminiService

router = APIRouter()

piapi   = PiAPIService()
catalog = get_catalog_service()
files   = FileHandler()

# Catalog folder is at backend/catalog/ — resolve relative to THIS file
# tryon.py is at backend/app/routes/tryon.py
# dirname x3 = backend/
BACKEND_DIR  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR  = os.path.join(BACKEND_DIR, "catalog")

# Cache to store statuses of Gemini background try-on tasks
gemini_tasks = {}


def run_gemini_tryon_background(task_id: str, user_path: str, item_path: str, prompt: str):
    """Background task to call Gemini Service and save output."""
    try:
        gemini_service = GeminiService()
        image_bytes = gemini_service.create_tryon_task(user_path, item_path, prompt)
        local_path = files.save_generated_image(image_bytes)
        
        # Upload to ImgBB for public URL so Video generation works
        public_url = None
        imgbb_key = os.getenv("IMGBB_KEY")
        if imgbb_key:
            import base64
            try:
                res = requests.post(
                    "https://api.imgbb.com/1/upload",
                    data={
                        "key": imgbb_key,
                        "image": base64.b64encode(image_bytes).decode('utf-8')
                    },
                    timeout=30
                )
                if res.status_code == 200:
                    public_url = res.json()["data"]["url"]
                    print(f"[Gemini Route] Uploaded to ImgBB: {public_url}")
                else:
                    print(f"[Gemini Route] ImgBB upload failed: {res.text}")
            except Exception as e:
                print(f"[Gemini Route] Failed to upload to ImgBB: {e}")

        gemini_tasks[task_id] = {
            "status": "completed",
            "local_path": local_path,
            "public_url": public_url
        }
    except Exception as e:
        print(f"[Gemini Route] Background try-on failed: {e}")
        gemini_tasks[task_id] = {
            "status": "failed",
            "error": str(e)
        }


@router.get("/catalog")
def get_catalog():
    """Returns all items with metadata for the frontend."""
    return catalog.get_all_items()


@router.post("/try-on")
async def start_tryon(
    background_tasks: BackgroundTasks,
    jewelry_id: str = Form(...),
    face_image: UploadFile = File(None),
    hand_image: UploadFile = File(None),
):
    jewelry = catalog.get_item_by_id(jewelry_id)
    if not jewelry:
        raise HTTPException(404, "Item not found in catalog")

    is_apparel = jewelry.get("category") == "apparel"
    jewelry_type = jewelry["type"]

    if not is_apparel and jewelry_type in ["ring", "bracelet", "bangle", "anklet"]:
        if not hand_image:
            raise HTTPException(400, "Hand image required for this jewellery type")
        user_img = hand_image
        img_type = "hand"
    else:
        if not face_image:
            raise HTTPException(400, "Portrait/body image required for this type")
        user_img = face_image
        img_type = "face"

    # Save the user upload and get its local path
    user_bytes = await user_img.read()
    user_path  = files.save_upload(user_bytes, img_type)

    # Resolve catalog image path
    jewelry_path = os.path.join(CATALOG_DIR, jewelry["image"])

    print(f"[try-on] user_path    = {user_path}")
    print(f"[try-on] jewelry_path = {jewelry_path}  exists={os.path.exists(jewelry_path)}")

    if not os.path.exists(jewelry_path):
        raise HTTPException(
            500,
            f"Catalog image not found at: {jewelry_path}."
        )

    # Route request based on category
    if is_apparel:
        # Apparel Try-on: run Gemini/Imagen pipeline in background
        prompt_data = build_apparel_prompt_with_context(
            apparel_type=jewelry.get("type", ""),
            apparel_name=jewelry.get("name", ""),
            apparel_material=jewelry.get("material", ""),
            apparel_color=jewelry.get("color", ""),
            apparel_fit=jewelry.get("fit", ""),
            apparel_pattern=jewelry.get("pattern", "")
        )
        
        task_id = f"gemini_{uuid.uuid4().hex}"
        gemini_tasks[task_id] = {"status": "processing"}
        background_tasks.add_task(run_gemini_tryon_background, task_id, user_path, jewelry_path, prompt_data["prompt"])
        return {
            "task_id": task_id,
            "status": "processing"
        }

    # Jewellery Try-on: run original PiAPI flow
    prompt_data = build_prompt_with_context(
        jewelry_type=jewelry["type"],
        jewelry_name=jewelry["name"],
        user_image_type=img_type,
        jewelry_material=jewelry.get("material", ""),
        jewelry_color=jewelry.get("color", ""),
        jewelry_style=jewelry.get("style", ""),
    )

    task = piapi.create_task(prompt_data, user_path, jewelry_path)

    if task.get("code") != 200:
        return {
            "status": "failed",
            "reason": task.get("error", {}).get("message", str(task)),
            "details": task,
        }

    return {
        "task_id": task["data"]["task_id"],
        "status":  "processing",
    }


@router.get("/try-on/{task_id}")
async def get_status(task_id: str, request: Request):
    # Handle Gemini tasks
    if task_id.startswith("gemini_"):
        task = gemini_tasks.get(task_id)
        if not task:
            return {"task_id": task_id, "status": "unknown"}
        
        status = task.get("status")
        if status == "completed":
            local_path = task.get("local_path")
            public_url = task.get("public_url")
            final_url = f"{request.base_url}{local_path}"
            
            public_base = os.getenv("PUBLIC_BASE_URL")
            if public_url:
                piapi_url = public_url
            elif public_base:
                piapi_url = f"{public_base.rstrip('/')}/{local_path}"
            else:
                piapi_url = final_url
                
            return {
                "task_id": task_id,
                "status": "completed",
                "image_url": final_url,
                "piapi_image_url": piapi_url # allow fallback for video generation
            }
        elif status == "failed":
            return {"task_id": task_id, "status": "failed", "error": task.get("error")}
        
        return {"task_id": task_id, "status": "processing"}

    # Handle standard PiAPI tasks
    result = piapi.get_task_status(task_id)
    if not result:
        return {"task_id": task_id, "status": "unknown"}

    data   = result.get("data", {})
    status = data.get("status")

    if status in ("success", "completed"):
        output    = data.get("output", {})
        image_url = output.get("image_url") or (output.get("image_urls") or [None])[0]

        try:
            img_resp = requests.get(image_url, timeout=30)
            img_resp.raise_for_status()
            local_path = files.save_generated_image(img_resp.content)
            final_url  = f"{request.base_url}{local_path}"
        except Exception as e:
            print("Failed to download generated image:", e)
            final_url = image_url

        return {
            "task_id":         task_id,
            "status":          "completed",
            "image_url":       final_url,
            "piapi_image_url": image_url,
        }

    if status == "failed":
        return {"task_id": task_id, "status": "failed", "error": result}

    return {"task_id": task_id, "status": "processing"}


from pydantic import BaseModel

class VideoRequest(BaseModel):
    image_url: str

@router.post("/generate-video")
async def generate_video(req: VideoRequest, request: Request):
    from app.services.video_service import VideoService
    if not req.image_url:
        raise HTTPException(400, "image_url is required")
    try:
        video_service = VideoService()
        video_task_id = video_service.create_video_task(req.image_url)
        video_result  = video_service.wait_for_video(video_task_id)
        video_url     = f"{request.base_url}{video_result['local_path']}"
        return {"status": "completed", "video_url": video_url}
    except Exception as e:
        print("Video generation failed:", e)
        return {"status": "failed", "error": str(e)}