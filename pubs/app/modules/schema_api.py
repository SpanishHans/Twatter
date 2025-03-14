from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ArchivoMultimediaBase(BaseModel):
    tipo_medio: str = Field(json_schema_extra={'examples': ['tipo'],})
    url_medio: str = Field(json_schema_extra={'examples': ['https://ubicacion/file.example'],})

class TwattBase(BaseModel):
    contenido: str = Field(json_schema_extra={'examples': ['https://ubicacion/file.example'],})
    es_recomparte: Optional[bool] = Field(default=False, json_schema_extra={'examples': ['False'],})
    id_publicacion_original: Optional[int] = Field(default=None, json_schema_extra={'examples': ['123'],})

class PublicacionCrear(TwattBase):
    archivos_multimedia: Optional[List[ArchivoMultimediaBase]] = Field(default=None, json_schema_extra={'examples': ['123','123'],})

class PublicacionRespuesta(TwattBase):
    id: int = Field(json_schema_extra={'examples': ['123'],})
    id_usuario: int = Field(json_schema_extra={'examples': ['123'],})
    fecha_creacion: datetime
    archivos_multimedia: Optional[List[ArchivoMultimediaBase]] = Field(default=None, json_schema_extra={'examples': ['123','123'],})

    model_config = {
        "from_attributes": True
    }