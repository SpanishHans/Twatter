import os
from fastapi import Request, HTTPException
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")  # Same as in auth container
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def decode_token(token: str, expected_type: str = "access"):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_type = payload.get("token_type")
        if token_type != expected_type:
            raise HTTPException(status_code=401, detail=f"Invalid token type: expected '{expected_type}', got '{token_type}'")

        return {
            "user_id": int(payload["sub"]),
            "username": payload["username"]
        }
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or malformed")

    token = auth_header[len("Bearer "):].strip()
    return decode_token(token, expected_type="access")
