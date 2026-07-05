import requests

from utils.config import (
    UPLOAD_ENDPOINT,
    ANALYZE_ENDPOINT,
    REQUEST_TIMEOUT,
)


class APIClient:

    @staticmethod
    def upload_file(file):

        files = {
            "file": (
                file.name,
                file.getvalue(),
                file.type,
            )
        }

        response = requests.post(
            UPLOAD_ENDPOINT,
            files=files,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def analyze(question: str):

        payload = {
            "question": question
        }

        response = requests.post(
            ANALYZE_ENDPOINT,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()