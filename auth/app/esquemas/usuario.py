from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre_usuario: constr(min_length=3, max_length=50)
    correo: EmailStr
    foto_perfil: Optional[str] = None
    biografia: Optional[str] = None

class UsuarioCrear(UsuarioBase):
    contrasena: constr(min_length=8)

class UsuarioRespuesta(UsuarioBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True