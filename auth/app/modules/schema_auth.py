from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Optional

from modules.schema_db import User_template

# Configuración de seguridad
SECRET_KEY = "tu-clave-secreta-muy-segura"  # Cambiar en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
        return pwd_context.verify(contrasena_plana, contrasena_hash)

    @staticmethod
    def crear_hash_contrasena(contrasena: str) -> str:
        return pwd_context.hash(contrasena)

    @staticmethod
    def crear_token_acceso(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verificar_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    def autenticar_usuario(db: Session, username: str, password: str) -> Optional[User_template]:
        usuario = db.query(User_template).filter(User_template.nombre_usuario == username).first()
        if not usuario:
            return None
        if not AuthService.verificar_contrasena(password, usuario.contrasena_hash):
            return None
        return usuario
