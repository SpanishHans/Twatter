from pydantic import BaseModel, Field
from datetime import datetime

class LikeBase(BaseModel):
    id_publicacion: int = Field(json_schema_extra={'examples': ['123'],})

class LikeTwatt(LikeBase):
    pass

class LikeRespuesta(LikeBase):
    id: int = Field(json_schema_extra={'examples': ['123'],})
    id_usuario: int = Field(json_schema_extra={'examples': ['123'],})
    fecha_creacion: datetime

class ComentarioBase(BaseModel):
    id_publicacion: int = Field(json_schema_extra={'examples': ['123'],})
    contenido: str = Field(min_length=3, max_length=30, json_schema_extra={'examples': ['juanjo23'],})

class Comment_Twatt(ComentarioBase):
    pass

class ComentarioRespuesta(ComentarioBase):
    id: int = Field(json_schema_extra={'examples': ['123'],})
    id_usuario: int = Field(json_schema_extra={'examples': ['123'],})
    fecha_creacion: datetime 