import os
import base64
from typing import Optional
import google.generativeai as genai


class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini service with API key."""
        api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_tryon_image(
        self,
        user_image_path: str,
        jewelry_image_path: str,
        prompt: str
    ) -> Optional[bytes]:
        """
        Generate virtual try-on image using Gemini.
        
        Args:
            user_image_path: Path to user's face or hand image
            jewelry_image_path: Path to jewelry image
            prompt: Detailed prompt for generation
        
        Returns:
            Generated image bytes or None if failed
        """
        try:
            # Read images and convert to base64
            with open(user_image_path, 'rb') as f:
                user_image_data = base64.standard_b64encode(f.read()).decode('utf-8')
            
            with open(jewelry_image_path, 'rb') as f:
                jewelry_image_data = base64.standard_b64encode(f.read()).decode('utf-8')
            
            # Prepare image parts
            image_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": user_image_data
                },
                {
                    "mime_type": "image/jpeg",
                    "data": jewelry_image_data
                }
            ]
            
            # Generate content with images
            full_prompt = f"""You have two images:
1. First image: The user's photo (face or hand)
2. Second image: The jewelry item to try on

{prompt}

Please create a photorealistic virtual try-on image combining these elements."""
            
            response = self.model.generate_content(
                [full_prompt] + image_parts
            )
            
            # Extract image from response if available
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if hasattr(candidate.content, 'parts') and len(candidate.content.parts) > 0:
                    part = candidate.content.parts[0]
                    if hasattr(part, 'inline_data') and part.inline_data:
                        return part.inline_data.data
            
            print(f"Response: {response.text}")
            return None
            
        except Exception as e:
            print(f"Error generating try-on image: {str(e)}")
            return None
    
    def get_available_models(self):
        """Get list of available Gemini models."""
        try:
            models = genai.list_models()
            return [m.name for m in models]
        except Exception as e:
            print(f"Error listing models: {str(e)}")
            return []
