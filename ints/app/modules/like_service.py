from sqlalchemy.orm import Session
from typing import List, Optional

from shared.models.like import Like

class LikeService:
    @staticmethod
    def dar_like(db: Session, id_usuario: int, id_publicacion: int) -> Optional[Like]:
        # Verificar si ya existe el like
        like_existente = db.query(Like).filter(
            Like.id_usuario == id_usuario,
            Like.id_publicacion == id_publicacion
        ).first()
        
        if like_existente:
            return None
        
        nuevo_like = Like(
            id_usuario=id_usuario,
            id_publicacion=id_publicacion
        )
        
        db.add(nuevo_like)
        db.commit()
        db.refresh(nuevo_like)
        
        return nuevo_like

    @staticmethod
    def quitar_like(db: Session, id_usuario: int, id_publicacion: int) -> bool:
        like = db.query(Like).filter(
            Like.id_usuario == id_usuario,
            Like.id_publicacion == id_publicacion
        ).first()
        
        if like:
            db.delete(like)
            db.commit()
            return True
        return False

    @staticmethod
    def obtener_likes_publicacion(db: Session, id_publicacion: int) -> List[Like]:
        return db.query(Like).filter(Like.id_publicacion == id_publicacion).all()