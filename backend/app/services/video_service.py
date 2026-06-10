import os
import time
import uuid
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class VideoService:
    def __init__(self):
        self.token = os.getenv("KLING_API_KEY")

        if not self.token:
            raise ValueError("KLING_API_KEY missing in .env")

        self.base_url = "https://api-singapore.klingai.com/v1/videos/image2video"

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # IMPORTANT: match YOUR structure
        self.base_dir = Path(__file__).parent.parent.parent
        self.video_dir = self.base_dir / "generated" / "videos"
        self.video_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # STEP 1: CREATE TASK
    # -----------------------------
    def create_video_task(self, image_path: str) -> str:

        image_base64 = self._to_base64(image_path)

        payload = {
            "model_name": "kling-v2-6",
            "image": image_base64,
            "prompt": (
                "Fashion try-on video. Subject naturally turns left and right with smooth motion. "
                "Subtle camera orbit, cinematic framing. Realistic lighting, soft shadows. "
                "High-quality commercial product video, stable and smooth motion."
            ),
            "duration": "5",
            "mode": "pro",
            "sound": "off"
    }

    # -----------------------------
    # STEP 2: POLL STATUS
    # -----------------------------
    def wait_for_video(self, task_id: str):
        url = f"{self.base_url}/{task_id}"

        while True:
            res = requests.get(url, headers=self.headers)
            res.raise_for_status()

            data = res.json()["data"]
            status = data["task_status"]

            print("Status:", status)

            if status == "succeed":
                video_url = data["task_result"]["videos"][0]["url"]
                return self._download(video_url)

            if status == "failed":
                raise Exception("Kling video generation failed")

            time.sleep(6)

    # -----------------------------
    # STEP 3: DOWNLOAD VIDEO
    # -----------------------------
    def _download(self, url: str) -> str:
        res = requests.get(url)
        res.raise_for_status()

        filename = f"video_{uuid.uuid4().hex[:10]}.mp4"
        path = self.video_dir / filename

        with open(path, "wb") as f:
            f.write(res.content)

        print("Saved video:", path)
        return str(path)

    # -----------------------------
    # UTIL: image → base64
    # -----------------------------
    def _to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        return f"data:image/png;base64,{encoded}"