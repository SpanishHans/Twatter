from sqlalchemy.orm import Session
from typing import List, Optional

from modelos.modelos import MeGusta

class LikeService:
    @staticmethod
    def dar_like(db: Session, id_usuario: int, id_publicacion: int) -> Optional[MeGusta]:
        # Verificar si ya existe el like
        like_existente = db.query(MeGusta).filter(
            MeGusta.id_usuario == id_usuario,
            MeGusta.id_publicacion == id_publicacion
        ).first()
        
        if like_existente:
            return None
        
        nuevo_like = MeGusta(
            id_usuario=id_usuario,
            id_publicacion=id_publicacion
        )
        
        db.add(nuevo_like)
        db.commit()
        db.refresh(nuevo_like)
        
        return nuevo_like

    @staticmethod
    def quitar_like(db: Session, id_usuario: int, id_publicacion: int) -> bool:
        like = db.query(MeGusta).filter(
            MeGusta.id_usuario == id_usuario,
            MeGusta.id_publicacion == id_publicacion
        ).first()
        
        if like:
            db.delete(like)
            db.commit()
            return True
        return False

    @staticmethod
    def obtener_likes_publicacion(db: Session, id_publicacion: int) -> List[MeGusta]:
        return db.query(MeGusta).filter(MeGusta.id_publicacion == id_publicacion).all()