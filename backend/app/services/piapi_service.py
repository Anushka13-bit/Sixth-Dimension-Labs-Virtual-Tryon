import os
import time
import base64
import requests


class PiAPIService:
    def __init__(self):
        self.api_key = os.getenv("PIAPI_KEY")
        self.base_url = os.getenv("PIAPI_BASE_URL")

        if not self.api_key:
            raise ValueError("PIAPI_KEY missing")

        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

    # convert image → base64
    def _encode(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    def create_task(self, prompt, user_image, jewelry_image):

        payload = {
            "model": "gemini",
            "task_type": "nano-banana-pro",
            "input": {
                "prompt": prompt,
                "image": user_image,
                "reference_image": jewelry_image,
                "aspect_ratio": "1:1",
                "output_format": "png"
            }
        }

        res = requests.post(self.base_url, json=payload, headers=self.headers)
        return res.json()

    def get_task(self, task_id):
        url = f"{self.base_url}/{task_id}"
        res = requests.get(url, headers=self.headers)
        return res.json()

    def generate_tryon(self, prompt, user_image_path, jewelry_image_path):

        user_img = self._encode(user_image_path)
        jewelry_img = self._encode(jewelry_image_path)

        task = self.create_task(prompt, user_img, jewelry_img)

        if task.get("code") != 200:
            return {"error": "task creation failed", "details": task}

        task_id = task["data"]["task_id"]

        for _ in range(40):
            result = self.get_task(task_id)
            data = result.get("data", {})

            if data.get("status") == "success":
                return {
                    "image_url": data["output"]["image_url"]
                }

            if data.get("status") == "failed":
                return {"error": "generation failed"}

            time.sleep(1)

        return {"error": "timeout"}