from __future__ import annotations

import requests

from utils.config import BACKEND_URL, REQUEST_TIMEOUT


class DashboardAPI:

    def __init__(self):
        self.base_url = f"{BACKEND_URL}/api"

    def build_dashboard(
        self,
        question: str,
    ):

        response = requests.post(
            f"{self.base_url}/dashboard",
            json={
                "question": question,
            },
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()


dashboard_api = DashboardAPI()