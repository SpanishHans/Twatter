import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
import uuid
from uuid import UUID

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")  # Same as in auth container
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes a password using bcrypt"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(hashed_password: str, password: str) -> bool:
        """Verifies a hashed password"""
        return pwd_context.verify(password, hashed_password)
    
    @staticmethod
    def generate_tokens(id: UUID, username: str):
        """Generates both Access and Refresh JWT tokens"""
        now = datetime.utcnow()
        access_expires = now + timedelta(minutes=15)
        refresh_expires = now + timedelta(days=7)
    
        jti = str(uuid.uuid4())  # Unique ID for refresh token
    
        access_payload = {
            "sub": str(id),
            "username": username,
            "exp": access_expires,
            "iat": now,
            "token_type": "access"
        }
    
        refresh_payload = {
            "sub": str(id),
            "username": username,
            "exp": refresh_expires,
            "iat": now,
            "jti": jti,
            "token_type": "refresh"
        }
    
        access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)
    
        return access_token, refresh_token
