from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pathlib import Path
import os

from app.services.catalog_service import get_catalog_service
from app.services.piapi_service import PiAPIService
from app.services.prompt_builder import build_prompt_with_context
from app.utils.file_handler import FileHandler

router = APIRouter()

file_handler = FileHandler()
catalog_service = get_catalog_service()
piapi = PiAPIService()


@router.get("/catalog")
def get_catalog():
    return catalog_service.get_all_items()


@router.post("/try-on")
async def try_on(
    jewelry_id: str = Form(...),
    face_image: UploadFile = File(None),
    hand_image: UploadFile = File(None)
):

    jewelry = catalog_service.get_item_by_id(jewelry_id)

    if not jewelry:
        raise HTTPException(404, "Jewelry not found")

    jewelry_type = jewelry["type"]

    # choose image
    if jewelry_type in ["ring", "bracelet"]:
        if not hand_image:
            raise HTTPException(400, "Hand image required")
        user_image = hand_image
        image_type = "hand"
    else:
        if not face_image:
            raise HTTPException(400, "Face image required")
        user_image = face_image
        image_type = "face"

    # save user image
    user_bytes = await user_image.read()
    user_path = file_handler.save_upload(user_bytes, image_type)

    jewelry_path = Path("catalog") / jewelry["image"]

    if not jewelry_path.exists():
        raise HTTPException(500, "Jewelry image missing")

    prompt = build_prompt_with_context(
        jewelry["type"],
        jewelry["name"],
        image_type
    )

    # ✅ REAL PIAPI CALL (image-to-image)
    result = piapi.generate_tryon(
        prompt=prompt,
        user_image_path=str(user_path),
        jewelry_image_path=str(jewelry_path)
    )

    if "error" in result:
        raise HTTPException(500, result["error"])

    return {
        "image_url": result["image_url"],
        "message": "Try-on generated successfully"
    }