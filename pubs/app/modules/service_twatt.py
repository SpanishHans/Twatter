import requests
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException

from shared.models.twatt import Twatt, Media

class TwattService:
    @staticmethod
    def crear_publicacion(
        db: Session, 
        id_usuario: int, 
        contenido: str, 
        es_recomparte: bool = False, 
        id_publicacion_original: Optional[int] = None,
        archivos_multimedia: Optional[List[dict]] = None
    ) -> Twatt:
        # Validar usuario con servicio de autenticación (simulado)
        nueva_publicacion = Twatt(
            id_usuario=id_usuario,
            contenido=contenido,
            es_recomparte=es_recomparte,
            id_publicacion_original=id_publicacion_original
        )
        
        db.add(nueva_publicacion)
        db.flush()  # Para obtener el ID de la publicación

        # Agregar archivos multimedia si existen
        if archivos_multimedia:
            for archivo in archivos_multimedia:
                multimedia = Media(
                    id_publicacion=nueva_publicacion.id,
                    tipo_medio=archivo['tipo_medio'],
                    url_medio=archivo['url_medio']
                )
                db.add(multimedia)
        
        db.commit()
        db.refresh(nueva_publicacion)
        
        return nueva_publicacion

    @staticmethod
    def obtener_publicaciones(
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Twatt]:
        return db.query(Twatt).offset(skip).limit(limit).all()

    @staticmethod
    def obtener_publicacion_por_id(
        db: Session, 
        publicacion_id: int
    ) -> Optional[Twatt]:
        publicacion = db.query(Twatt).filter(Twatt.id == publicacion_id).first()
        if not publicacion:
            raise HTTPException(status_code=404, detail="Publicación no encontrada")
        return publicacion

    @staticmethod
    def eliminar_publicacion(
        db: Session, 
        publicacion_id: int, 
        id_usuario: int
    ) -> bool:
        publicacion = db.query(Twatt).filter(
            Twatt.id == publicacion_id, 
            Twatt.id_usuario == id_usuario
        ).first()
        
        if not publicacion:
            raise HTTPException(status_code=404, detail="Publicación no encontrada")
        
        db.delete(publicacion)
        db.commit()
        return True