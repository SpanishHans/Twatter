from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LikeBase(BaseModel):
    id_publicacion: int

class LikeCrear(LikeBase):
    pass

class LikeRespuesta(LikeBase):
    id: int
    id_usuario: int
    fecha_creacion: datetime

class ComentarioBase(BaseModel):
    id_publicacion: int
    contenido: str

class ComentarioCrear(ComentarioBase):
    pass

class ComentarioRespuesta(ComentarioBase):
    id: int
    id_usuario: int
    fecha_creacion: datetime