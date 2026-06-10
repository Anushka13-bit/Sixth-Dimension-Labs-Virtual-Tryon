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

    def _encode(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    # -----------------------
    # CREATE TASK ONLY
    # -----------------------
    def create_task(self, prompt, user_image, jewelry_image):

        payload = {
            "model": "gemini",
            "task_type": "nano-banana-2",
            "input": {
                "prompt": prompt,
                "image": user_image,
                "reference_image": jewelry_image,
                "aspect_ratio": "1:1",
                "output_format": "png"
            }
        }

        res = requests.post(self.base_url, json=payload, headers=self.headers, timeout=30)
        return res.json()

    # -----------------------
    # GET TASK STATUS
    # -----------------------
    def get_task_status(self, task_id):

        url = f"{self.base_url}/{task_id}"

        res = requests.get(url, headers=self.headers, timeout=30)
        return res.json()