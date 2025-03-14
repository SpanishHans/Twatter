from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Request, HTTPException
from jose import jwt

# Configuración de seguridad
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes a password using bcrypt"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verifies a hashed password"""
        return pwd_context.verify(password, hashed_password)

    @staticmethod
    def generate_token(usuario_id: int, username: str):
        """Generates JWT access token with user ID and username"""
        expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(usuario_id),
            "username": username,
            "exp": expira,
            "iat": datetime.utcnow(),  # Issued at
            "token_type": "access"
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(request: Request):
        """Validates JWT from cookies (for same subdomain microservices)."""
        token = request.cookies.get("access_token")

        if not token:
            raise HTTPException(status_code=401, detail="Token missing")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            username = payload.get("username")

            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token structure")

            return {"user_id": user_id, "username": username}

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")