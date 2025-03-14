import requests
from fastapi import HTTPException, Request

AUTH_SERVICE_URL = "http://auth-service:8000/verify-token"  # Auth service URL

def get_current_user(request: Request):
    """Calls auth service to verify user based on cookies."""
    cookies = request.cookies  # Cookies are automatically sent
    response = requests.get(AUTH_SERVICE_URL, cookies=cookies)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Authentication failed")

    return response.json()