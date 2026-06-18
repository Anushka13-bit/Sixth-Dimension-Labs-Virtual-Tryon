import os
import time
import uuid
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class VideoService:
    def __init__(self):
        # -------------------------
        # AUTH (BEARER TOKEN)
        # -------------------------
        self.api_key = os.getenv("KIE_API_KEY")

        if not self.api_key:
            raise ValueError("KIE_API_KEY missing in .env")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # -------------------------
        # ENDPOINTS
        # -------------------------
        self.create_url = "https://api.kie.ai/api/v1/jobs/createTask"
        self.status_url = "https://api.kie.ai/api/v1/jobs/recordInfo"

        # -------------------------
        # STORAGE
        # -------------------------
        self.base_dir = Path(__file__).parent.parent.parent
        self.video_dir = self.base_dir / "generated" / "videos"
        self.video_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------
    # CREATE TASK
    # -------------------------
    def create_video_task(self, image_url: str) -> str:
        payload = {
            "model": "kling-2.6/image-to-video",
            "input": {
                "image_urls": [image_url],
                "prompt": (
                    "Fashion try-on video. Subject naturally turns left and right with smooth motion. "
                    "Subtle camera orbit, cinematic framing. Realistic lighting, soft shadows. "
                    "High-quality commercial product video, stable and smooth motion."
                ),
                "duration": "5",
                "sound": False 
            }
        }

        res = requests.post(
            self.create_url,
            json=payload,
            headers=self.headers,
            timeout=30
        )

        raw = self._safe_json(res)

        print("[CREATE RESPONSE]", raw)

        # ❌ HARD GUARD: no data at all
        if not isinstance(raw, dict):
            raise Exception(f"Invalid API response: {raw}")

        # ❌ API error case
        if raw.get("code") not in (None, 200):
            raise Exception(f"API Error: {raw}")

        data = raw.get("data")
        if not isinstance(data, dict):
            raise Exception(f"No data returned: {raw}")

        task_id = data.get("taskId")
        if not task_id:
            raise Exception(f"No taskId found: {raw}")

        print("[VideoService] Task ID:", task_id)
        return task_id

    # -------------------------
    # POLL TASK
    # -------------------------
    def wait_for_video(self, task_id: str, max_wait: int = 400):
        start = time.time()

        while time.time() - start < max_wait:

            res = requests.get(
                self.status_url,
                headers=self.headers,
                params={"taskId": task_id},
                timeout=30
            )

            raw = self._safe_json(res)

            print("[STATUS RESPONSE]", raw)

            if not isinstance(raw, dict):
                raise Exception(f"Invalid status response: {raw}")

            data = raw.get("data")
            if not isinstance(data, dict):
                # STILL SAFE: don't crash
                raise Exception(f"Missing data in status response: {raw}")

            state = data.get("state")
            print(f"[VideoService] State: {state}")

            # ---------------- SUCCESS ----------------
            if state == "success":
                import json
                result_json = data.get("resultJson", "{}")
                video_url = None
                try:
                    parsed = json.loads(result_json)
                    video_url = parsed.get("resultUrls", [None])[0]
                except Exception as e:
                    print("Error parsing resultJson:", e)

                if not video_url:
                    raise Exception(f"No video URL found in resultJson: {data}")

                return {
                    "video_url": video_url,
                    "local_path": self._download(video_url)
                }

            # ---------------- FAILURE ----------------
            if state == "fail":
                raise Exception(f"Generation failed: {data}")

            time.sleep(5)

        raise Exception("Timeout waiting for video generation")

    # -------------------------
    # SAFE JSON PARSER
    # -------------------------
    def _safe_json(self, res):
        try:
            return res.json()
        except Exception:
            return {
                "error": "Invalid JSON response",
                "raw": res.text
            }

    # -------------------------
    # DOWNLOAD
    # -------------------------
    def _download(self, url: str) -> str:
        res = requests.get(url)
        res.raise_for_status()

        filename = f"video_{uuid.uuid4().hex[:10]}.mp4"
        path = self.video_dir / filename

        with open(path, "wb") as f:
            f.write(res.content)

        print("[VideoService] Saved:", path)

        return f"generated/videos/{filename}"