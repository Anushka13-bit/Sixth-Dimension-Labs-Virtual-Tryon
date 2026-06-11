import os
import requests
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from app.services.piapi_service import PiAPIService
from app.services.prompt_builder import build_prompt_with_context
from app.services.catalog_service import get_catalog_service
from app.utils.file_handler import FileHandler

router = APIRouter()

piapi   = PiAPIService()
catalog = get_catalog_service()
files   = FileHandler()

# Catalog folder is at backend/catalog/ — resolve relative to THIS file
# tryon.py is at backend/app/routes/tryon.py
# dirname x3 = backend/
BACKEND_DIR  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR  = os.path.join(BACKEND_DIR, "catalog")


@router.get("/catalog")
def get_catalog():
    """Returns all jewellery items with metadata for the frontend."""
    return catalog.get_all_items()


@router.post("/try-on")
async def start_tryon(
    jewelry_id: str = Form(...),
    face_image: UploadFile = File(None),
    hand_image: UploadFile = File(None),
):
    jewelry = catalog.get_item_by_id(jewelry_id)
    if not jewelry:
        raise HTTPException(404, "Jewelry not found")

    jewelry_type = jewelry["type"]

    if jewelry_type in ["ring", "bracelet", "bangle", "anklet"]:
        if not hand_image:
            raise HTTPException(400, "Hand image required for this jewellery type")
        user_img = hand_image
        img_type = "hand"
    else:
        if not face_image:
            raise HTTPException(400, "Face/portrait image required for this jewellery type")
        user_img = face_image
        img_type = "face"

    # Save the user upload and get its local path
    user_bytes = await user_img.read()
    user_path  = files.save_upload(user_bytes, img_type)

    # Resolve jewellery image path — catalog/ is a sibling of app/
    jewelry_path = os.path.join(CATALOG_DIR, jewelry["image"])

    print(f"[try-on] user_path    = {user_path}")
    print(f"[try-on] jewelry_path = {jewelry_path}  exists={os.path.exists(jewelry_path)}")

    if not os.path.exists(jewelry_path):
        raise HTTPException(
            500,
            f"Jewellery image not found at: {jewelry_path}. "
            f"Available files: {os.listdir(CATALOG_DIR) if os.path.exists(CATALOG_DIR) else 'CATALOG_DIR missing'}"
        )

    # Build the natural-language prompt with all catalog metadata
    prompt_data = build_prompt_with_context(
        jewelry_type=jewelry["type"],
        jewelry_name=jewelry["name"],
        user_image_type=img_type,
        jewelry_material=jewelry.get("material", ""),
        jewelry_color=jewelry.get("color", ""),
        jewelry_style=jewelry.get("style", ""),
    )

    # piapi_service uploads both images to CDN internally and returns public URLs
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