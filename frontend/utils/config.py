import os

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://ai-data-analyst-api-mui0.onrender.com"
)

UPLOAD_ENDPOINT = f"{BACKEND_URL}/api/upload"
ANALYZE_ENDPOINT = f"{BACKEND_URL}/api/analyze"

REQUEST_TIMEOUT = 120