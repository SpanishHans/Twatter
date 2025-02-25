from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ArchivoMultimediaBase(BaseModel):
    tipo_medio: str
    url_medio: str

class PublicacionBase(BaseModel):
    contenido: str
    es_recomparte: Optional[bool] = False
    id_publicacion_original: Optional[int] = None

class PublicacionCrear(PublicacionBase):
    archivos_multimedia: Optional[List[ArchivoMultimediaBase]] = None

class PublicacionRespuesta(PublicacionBase):
    id: int
    id_usuario: int
    fecha_creacion: datetime
    archivos_multimedia: Optional[List[ArchivoMultimediaBase]] = None

    class Config:
        orm_mode = True