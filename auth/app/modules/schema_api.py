from pydantic import BaseModel, EmailStr, SecretStr, Field
from typing import Optional

class UsuarioBase(BaseModel):
    nombre_usuario: str = Field(min_length=3, max_length=30, json_schema_extra={'examples': ['juanjo23'],})
    correo: EmailStr = Field(json_schema_extra={'examples': ['juan@example.com'],})
    foto_perfil: Optional[str] = Field(json_schema_extra={'examples': ['https://example.com/profile.jpg'],})
    biografia: Optional[str] = Field(json_schema_extra={'examples': ['Apasionado por la tecnología y la innovación.'],})

class UsuarioNuevo(UsuarioBase):
    contrasena: SecretStr = Field(min_length=3, max_length=30, json_schema_extra={'examples': ['SecureP@ssw0rd'],})

class UsuarioLogin(BaseModel):
    nombre_usuario: str = Field(min_length=3, max_length=30, json_schema_extra={'examples': ['juanjo23'],})
    contrasena: SecretStr = Field(min_length=3, max_length=30, json_schema_extra={'examples': ['SecureP@ssw0rd'],})





class Token(BaseModel):
    token_access: str = Field(json_schema_extra={'examples': ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'],})
    token_type: str = Field(json_schema_extra={'examples': ['bearer'],})





# class UsuarioRespuesta(UsuarioBase):
#     id: int
#     fecha_creacion: datetime
#     fecha_actualizacion: datetime

#     model_config = {
#         "from_attributes": True
#     }

# class UsuarioBusqueda(BaseModel):
#     nombre_usuario: Optional[str] = None
#     skip: int = 0
#     limit: int = 100