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

    if status == "success":
        # Download the image from piapi and save it to the generated folder
        image_url = data["output"]["image_url"]
        try:
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            local_path = files.save_generated_image(img_response.content)
            
            final_image_url = f"{request.base_url}{local_path}"
        except Exception as e:
            print("Failed to download image:", e)
            final_image_url = image_url

        return {
            "task_id": task_id,
            "status": "completed",
            "image_url": final_image_url
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