import os
import requests
import mimetypes
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()


class PiAPIService:
    def __init__(self):
        self.api_key = os.getenv("PIAPI_KEY")
        self.base_url = os.getenv("PIAPI_BASE_URL")
        if not self.api_key:
            raise ValueError("PIAPI_KEY missing")

        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        )

        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def _upscale_if_needed(self, image_path: str, min_dimension: int = 512) -> str:
        try:
            from PIL import Image
            import tempfile

            img = Image.open(image_path)
            w, h = img.size
            print(f"  Image size: {w}x{h}")

            if w < min_dimension or h < min_dimension:
                scale = min_dimension / min(w, h)
                new_w, new_h = int(w * scale), int(h * scale)
                img = img.resize((new_w, new_h), Image.LANCZOS)
                ext = os.path.splitext(image_path)[1] or ".jpg"
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
                img.save(tmp.name, quality=92)
                print(f"  Upscaled {w}x{h} → {new_w}x{new_h}: {tmp.name}")
                return tmp.name
        except ImportError:
            print("  PIL not available — skipping upscale")
        except Exception as e:
            print(f"  Upscale failed ({e}) — using original")
        return image_path

    def _upload_image(self, file_path: str) -> str:
        """
        Upload image to Cloudinary and return a public HTTPS URL.
        No hotlink blocking, works with all external APIs.
        """
        result = cloudinary.uploader.upload(
            file_path,
            folder="virtual-tryon",
            resource_type="image",
        )
        url = result["secure_url"]
        print(f"  Uploaded {os.path.basename(file_path)} → {url}")
        return url

    def create_task(
        self,
        prompt_data,
        user_image_path: str,
        jewelry_image_path: str,
    ):
        if isinstance(prompt_data, dict):
            prompt = prompt_data.get("prompt", "")
        else:
            prompt = str(prompt_data)

        for label, path in [("user", user_image_path), ("jewellery", jewelry_image_path)]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"{label} image not found: {path}")
            size = os.path.getsize(path)
            print(f"  [{label}] {path} — {size:,} bytes")

        jewelry_image_path = self._upscale_if_needed(jewelry_image_path, min_dimension=512)
        user_image_path    = self._upscale_if_needed(user_image_path, min_dimension=512)

        print("Uploading images to Cloudinary...")
        user_url    = self._upload_image(user_image_path)
        jewelry_url = self._upload_image(jewelry_image_path)

        payload = {
            "model": "gemini",
            "task_type": "nano-banana-2",
            "input": {
                "prompt": prompt,
                "image_urls": [
                    user_url,
                    jewelry_url,
                ],
                "resolution": "1K",
                "aspect_ratio": "1:1",
                "output_format": "png",
            },
        }

        print("=== PIAPI PAYLOAD ===")
        print("PROMPT:", prompt)
        print(f"image_urls[0] (person):    {user_url}")
        print(f"image_urls[1] (jewellery): {jewelry_url}")

        res = requests.post(
            self.base_url,
            json=payload,
            headers=self.headers,
            timeout=30,
        )
        print("STATUS:", res.status_code)
        print("FULL BODY:", res.text)
        return res.json()

    def get_task_status(self, task_id: str):
        url = f"{self.base_url}/{task_id}"
        res = requests.get(url, headers=self.headers, timeout=30)
        return res.json()