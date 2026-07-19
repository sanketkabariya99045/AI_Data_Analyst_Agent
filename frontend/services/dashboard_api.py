"""
frontend/services/dashboard_api.py

Dashboard API Client

Author:
Sanket Kabariya
"""

from __future__ import annotations

import requests


class DashboardAPI:

    def __init__(self):

        self.base_url = "http://127.0.0.1:8000/api"

    # -----------------------------------------------------

    def build_dashboard(
        self,
        question: str,
    ):

        response = requests.post(

            f"{self.base_url}/dashboard",

            json={

                "question": question,

            },

            timeout=120,

        )

        response.raise_for_status()

        return response.json()


# =======================================================
# Singleton
# =======================================================

dashboard_api = DashboardAPI()