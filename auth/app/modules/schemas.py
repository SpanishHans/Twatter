from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing import Optional

class UsuarioBase(BaseModel):
    correo: EmailStr = Field(json_schema_extra={'examples': ['juan@example.com']})
    foto_perfil: Optional[str] = Field(None, json_schema_extra={'examples': ['https://example.com/profile.jpg']})
    biografia: Optional[str] = Field(None, json_schema_extra={'examples': ['Apasionado por la tecnología y la innovación.']})

class UsuarioCredenciales(BaseModel):
    nombre_usuario: str = Field(min_length=3, max_length=30, json_schema_extra={'examples': ['juanjo23']})
    contrasena: SecretStr = Field(min_length=3, max_length=30, json_schema_extra={'examples': ['SecureP@ssw0rd']})

class UsuarioNuevo(UsuarioBase, UsuarioCredenciales):
    pass

class UsuarioLogin(UsuarioCredenciales):
    pass
