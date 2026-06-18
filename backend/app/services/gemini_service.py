import os
import base64
import requests
import mimetypes
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY missing in environment variables")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def _get_base64_image(self, file_path: str) -> tuple[str, str]:
        """Reads image and returns (base64_string, mime_type)."""
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "image/jpeg"
        with open(file_path, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode("utf-8")
        return b64_data, mime_type

    def create_tryon_task(self, user_image_path: str, apparel_image_path: str, prompt_text: str) -> bytes:
        """
        Executes the try-on pipeline:
        Uses Nano Banana 2 (gemini-3.1-flash-image).
        Returns raw image bytes.
        """
        user_b64, user_mime = self._get_base64_image(user_image_path)
        apparel_b64, apparel_mime = self._get_base64_image(apparel_image_path)

        model = "gemini-3.1-flash-image"
        print(f"[GeminiService] Attempting try-on with {model} (Nano Banana 2)...")
        url = f"{self.base_url}/models/{model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{
                "parts": [
                    {"inline_data": {"mime_type": user_mime, "data": user_b64}},
                    {"inline_data": {"mime_type": apparel_mime, "data": apparel_b64}},
                    {"text": prompt_text}
                ]
            }],
            "generationConfig": {
                "responseModalities": ["IMAGE"]
            }
        }
        
        try:
            res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=45)
            if res.status_code == 200:
                data = res.json()
                # Parse image from response candidates
                parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                for part in parts:
                    if "inlineData" in part and "data" in part["inlineData"]:
                        print(f"[GeminiService] Successfully generated try-on via {model}!")
                        return base64.b64decode(part["inlineData"]["data"])
                    elif "inline_data" in part and "data" in part["inline_data"]:
                        print(f"[GeminiService] Successfully generated try-on via {model}!")
                        return base64.b64decode(part["inline_data"]["data"])
                    elif "text" in part and len(part["text"]) > 1000:
                        # Fallback just in case the model returns pure base64 in text part
                        try:
                            decoded = base64.b64decode(part["text"].strip())
                            print(f"[GeminiService] Successfully generated try-on via {model} (text fallback)!")
                            return decoded
                        except Exception:
                            pass
                
                # If we get here, it means 200 OK but no image data in the response
                error_msg = f"API returned 200 OK, but no image data found. Response: {data}"
                print(f"[GeminiService] {error_msg}")
                raise RuntimeError(error_msg)
            else:
                error_msg = f"API returned error: {res.status_code} {res.text}"
                print(f"[GeminiService] {error_msg}")
                raise RuntimeError(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Request to Gemini API failed: {e}"
            print(f"[GeminiService] {error_msg}")
            raise RuntimeError(error_msg)
