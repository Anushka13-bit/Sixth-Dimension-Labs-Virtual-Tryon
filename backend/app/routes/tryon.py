from fastapi import APIRouter, File, UploadFile, Form, HTTPException, BackgroundTasks
from pathlib import Path
import os
import mimetypes

from ..models.schemas import TryOnResponse, ErrorResponse, JewelryItem
from ..services.gemini_service import GeminiService
from ..services.video_service import get_video_service
from ..services.catalog_service import get_catalog_service
from ..services.prompt_builder import build_prompt_with_context
from ..utils.file_handler import FileHandler

router = APIRouter()
file_handler = FileHandler()
video_service = get_video_service()
catalog_service = get_catalog_service()


@router.get("/catalog", response_model=list[JewelryItem])
async def get_catalog():
    """
    Get all jewelry items in the catalog.
    
    Returns:
        List of jewelry items
    """
    items = catalog_service.get_all_items()
    return items


@router.post("/try-on", response_model=TryOnResponse)
async def try_on(
    jewelry_id: str = Form(...),
    face_image: UploadFile = File(None),
    hand_image: UploadFile = File(None)
):
    """
    Virtual try-on endpoint.
    
    Args:
        jewelry_id: ID of the jewelry item from catalog
        face_image: Optional face image file
        hand_image: Optional hand image file
    
    Returns:
        Generated image URL and video URL
    
    Raises:
        HTTPException: If validation fails or generation fails
    """
    
    try:
        # Load jewelry from catalog
        jewelry = catalog_service.get_item_by_id(jewelry_id)
        if not jewelry:
            raise HTTPException(
                status_code=404,
                detail=f"Jewelry item with ID {jewelry_id} not found"
            )
        
        jewelry_type = jewelry.get('type')
        jewelry_name = jewelry.get('name')
        
        # Validate image requirements based on jewelry type
        if jewelry_type in ['ring', 'bracelet']:
            if not hand_image:
                raise HTTPException(
                    status_code=400,
                    detail=f"Hand image required for {jewelry_type} try-on"
                )
            user_image = hand_image
            user_image_type = 'hand'
        elif jewelry_type in ['necklace', 'earrings']:
            if not face_image:
                raise HTTPException(
                    status_code=400,
                    detail=f"Face image required for {jewelry_type} try-on"
                )
            user_image = face_image
            user_image_type = 'face'
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown jewelry type: {jewelry_type}"
            )
        
        # Save uploaded images
        user_image_content = await user_image.read()
        user_image_path = file_handler.save_upload(user_image_content, user_image_type)
        
        # Get jewelry image from catalog
        jewelry_image_path = Path(__file__).parent.parent.parent / "catalog" / jewelry.get('image')
        if not jewelry_image_path.exists():
            # Create placeholder if it doesn't exist
            jewelry_image_path = Path(__file__).parent.parent.parent / "catalog" / "placeholder.jpg"
            if not jewelry_image_path.exists():
                raise HTTPException(
                    status_code=500,
                    detail="Jewelry image not found"
                )
        
        # Build prompt
        prompt = build_prompt_with_context(jewelry_type, jewelry_name, user_image_type)
        
        # Generate image using Gemini
        gemini_service = GeminiService()
        generated_image_bytes = gemini_service.generate_tryon_image(
            user_image_path,
            str(jewelry_image_path),
            prompt
        )
        
        if not generated_image_bytes:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate try-on image"
            )
        
        # Save generated image
        generated_image_path = file_handler.save_generated_image(generated_image_bytes)
        
        # Generate video
        video_path = video_service.generate_video(generated_image_path)
        
        # Construct URLs
        backend_url = os.getenv('BACKEND_URL', 'http://localhost:8000')
        image_url = file_handler.get_generated_url(generated_image_path, backend_url)
        video_url = file_handler.get_generated_url(video_path, backend_url)
        
        return TryOnResponse(
            image_url=image_url,
            video_url=video_url,
            message="Try-on image generated successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in try-on endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
