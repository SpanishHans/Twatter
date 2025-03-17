from sqlalchemy.orm import Session
from typing import List

from shared.models.comment import Comment

class CommentService:
    @staticmethod
    def crear_comentario(db: Session, id_usuario: int, id_publicacion: int, contenido: str) -> Comment:
        nuevo_comentario = Comment(
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
        comentario = db.query(Comment).filter(
            Comment.id == id_comentario,
            Comment.id_usuario == id_usuario
        ).first()
        
        if comentario:
            db.delete(comentario)
            db.commit()
            return True
        return False

    @staticmethod
    def obtener_comentarios_publicacion(db: Session, id_publicacion: int) -> List[Comment]:
        return db.query(Comment).filter(Comment.id_publicacion == id_publicacion).all()