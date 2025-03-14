from sqlalchemy.orm import Session
from typing import List

from modules.schema_db import Comentario

class ComentarioService:
    @staticmethod
    def crear_comentario(db: Session, id_usuario: int, id_publicacion: int, contenido: str) -> Comentario:
        nuevo_comentario = Comentario(
            id_usuario=id_usuario,
            id_publicacion=id_publicacion,
            contenido=contenido
        )
        
        db.add(nuevo_comentario)
        db.commit()
        db.refresh(nuevo_comentario)
        
        return nuevo_comentario

    @staticmethod
    def eliminar_comentario(db: Session, id_comentario: int, id_usuario: int) -> bool:
        comentario = db.query(Comentario).filter(
            Comentario.id == id_comentario,
            Comentario.id_usuario == id_usuario
        ).first()
        
        if comentario:
            db.delete(comentario)
            db.commit()
            return True
        return False

    @staticmethod
    def obtener_comentarios_publicacion(db: Session, id_publicacion: int) -> List[Comentario]:
        return db.query(Comentario).filter(Comentario.id_publicacion == id_publicacion).all()