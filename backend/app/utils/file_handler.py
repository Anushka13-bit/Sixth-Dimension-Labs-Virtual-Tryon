import os
import uuid
from datetime import datetime
from pathlib import Path
from PIL import Image


class FileHandler:
    def __init__(self):
        self.uploads_dir = Path(__file__).parent.parent.parent / "uploads"
        self.generated_dir = Path(__file__).parent.parent.parent / "generated"
        
        # Create directories if they don't exist
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.generated_dir.mkdir(parents=True, exist_ok=True)
    
    def save_upload(self, file_content: bytes, file_type: str) -> str:
        """
        Save uploaded file and return the path.
        
        Args:
            file_content: File bytes
            file_type: Type of file (face_image, hand_image, jewelry_image)
        
        Returns:
            File path relative to uploads directory
        """
        filename = f"{file_type}_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = self.uploads_dir / filename
        
        # Save the file
        with open(filepath, 'wb') as f:
            f.write(file_content)
        
        return str(filepath)
    
    def save_generated_image(self, image_content: bytes) -> str:
        """
        Save generated image from Gemini.
        
        Args:
            image_content: Image bytes
        
        Returns:
            File path relative to generated directory
        """
        filename = f"generated_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = self.generated_dir / filename
        
        with open(filepath, 'wb') as f:
            f.write(image_content)
        
        return str(filepath)
    
    def get_file_bytes(self, filepath: str) -> bytes:
        """Read file bytes."""
        with open(filepath, 'rb') as f:
            return f.read()
    
    def validate_image(self, filepath: str) -> bool:
        """Validate if file is a valid image."""
        try:
            img = Image.open(filepath)
            img.verify()
            return True
        except Exception:
            return False
    
    def get_upload_url(self, filepath: str, base_url: str) -> str:
        """Convert filepath to URL."""
        relative_path = os.path.relpath(filepath, Path(__file__).parent.parent.parent)
        return f"{base_url}/{relative_path.replace(os.sep, '/')}"
    
    def get_generated_url(self, filepath: str, base_url: str) -> str:
        """Convert generated filepath to URL."""
        relative_path = os.path.relpath(filepath, Path(__file__).parent.parent.parent)
        return f"{base_url}/{relative_path.replace(os.sep, '/')}"
