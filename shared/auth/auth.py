import requests
from fastapi import HTTPException, Request

AUTH_SERVICE_URL = "http://auth:8000/verify-token"

def get_current_user(request: Request):
    """Calls external auth service to verify user based on cookies."""
    cookies = request.cookies
    try:
        response = requests.get(AUTH_SERVICE_URL, cookies=cookies, timeout=3)
        response.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Auth service unavailable")

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="User is not logged in")

    user_data = response.json()

    if "user_id" not in user_data:
        raise HTTPException(status_code=401, detail="Authentication failed: User ID missing")

    # Ensure user_id is an integer, even if it's a string
    try:
        user_data["user_id"] = int(user_data["user_id"])
    except ValueError:
        raise HTTPException(status_code=401, detail="Authentication failed: Invalid User ID")

    return user_data
