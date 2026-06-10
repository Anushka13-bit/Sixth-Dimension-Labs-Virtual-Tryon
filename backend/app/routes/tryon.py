import requests
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Request
from app.services.piapi_service import PiAPIService
from app.services.prompt_builder import build_prompt_with_context
from app.services.catalog_service import get_catalog_service
from app.utils.file_handler import FileHandler

router = APIRouter()

piapi = PiAPIService()
catalog = get_catalog_service()
files = FileHandler()


@router.get("/catalog")
def get_catalog():
    return catalog.get_all_items()


# ---------------------------
# 1. START GENERATION
# ---------------------------
@router.post("/try-on")
async def start_tryon(
    jewelry_id: str = Form(...),
    face_image: UploadFile = File(None),
    hand_image: UploadFile = File(None)
):

    jewelry = catalog.get_item_by_id(jewelry_id)

    if not jewelry:
        raise HTTPException(404, "Jewelry not found")

    jewelry_type = jewelry["type"]

    # choose image
    if jewelry_type in ["ring", "bracelet"]:
        if not hand_image:
            raise HTTPException(400, "Hand image required")
        user_img = hand_image
        img_type = "hand"
    else:
        if not face_image:
            raise HTTPException(400, "Face image required")
        user_img = face_image
        img_type = "face"

    # save images
    user_bytes = await user_img.read()
    user_path = files.save_upload(user_bytes, img_type)

    jewelry_path = f"catalog/{jewelry['image']}"

    prompt = build_prompt_with_context(
        jewelry["type"],
        jewelry["name"],
        img_type
    )

    # encode images
    user_encoded = piapi._encode(user_path)
    jewelry_encoded = piapi._encode(jewelry_path)

    task = piapi.create_task(prompt, user_encoded, jewelry_encoded)

    if task.get("code") != 200:
        if task.get("error"):
            return {
            "status": "failed",
            "reason": task["error"].get("message"),
            "details": task
        }

    return {
        "task_id": task["data"]["task_id"],
        "status": "processing"
    }


# ---------------------------
# 2. CHECK STATUS
# ---------------------------
@router.get("/try-on/{task_id}")
async def get_status(task_id: str, request: Request):

    result = piapi.get_task_status(task_id)

    if not result:
        return {
            "task_id": task_id,
            "status": "unknown"
        }

    data = result.get("data", {})
    status = data.get("status")

    if status in ["success", "completed"]:
        # Download the image from PiAPI and save it to the generated folder
        output = data.get("output", {})
        image_url = output.get("image_url")
        if not image_url and "image_urls" in output and len(output["image_urls"]) > 0:
            image_url = output["image_urls"][0]

        local_path = None
        try:
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            local_path = files.save_generated_image(img_response.content)
            final_image_url = f"{request.base_url}{local_path}"
        except Exception as e:
            print("Failed to download generated image:", e)
            final_image_url = image_url

        # Return image immediately — video is generated separately
        return {
            "task_id": task_id,
            "status": "completed",
            "image_url": final_image_url,
            "piapi_image_url": image_url
        }

    if status == "failed":
        return {
            "task_id": task_id,
            "status": "failed",
            "error": result
        }

    return {
        "task_id": task_id,
        "status": "processing"
    }


from pydantic import BaseModel

class VideoRequest(BaseModel):
    image_url: str

# ---------------------------
# 3. GENERATE VIDEO (separate step)
# ---------------------------
@router.post("/generate-video")
async def generate_video(req: VideoRequest, request: Request):
    """
    Accepts { "image_url": "..." } and creates a Kling video.
    Returns the video URL once done.
    """
    from app.services.video_service import VideoService

    image_url = req.image_url

    if not image_url:
        raise HTTPException(400, "image_url is required")

    try:
        video_service = VideoService()
        video_task_id = video_service.create_video_task(image_url)
        video_result = video_service.wait_for_video(video_task_id)
        video_url = f"{request.base_url}{video_result['local_path']}"

        return {
            "status": "completed",
            "video_url": video_url
        }
    except Exception as e:
        print("Video generation failed:", e)
        return {
            "status": "failed",
            "error": str(e)
        }