"""
Application configuration.
"""

BACKEND_URL = "http://127.0.0.1:8000"

UPLOAD_ENDPOINT = f"{BACKEND_URL}/api/upload"
ANALYZE_ENDPOINT = f"{BACKEND_URL}/api/analyze"

REQUEST_TIMEOUT = 120