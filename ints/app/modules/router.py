from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

import requests

from shared.db.db_engine import get_db
from shared.auth.auth import get_current_user

from modules.service_like import LikeService
from modules.service_comm import CommentService
from modules.schemas import LikeTwatt, Comment_Twatt, LikeRespuesta, ComentarioRespuesta


router = APIRouter(tags=["Interacciones"])

@router.post("/like", response_model=LikeRespuesta)
def dar_like(
    like: LikeTwatt,  
    request: Request,
    db: Session = Depends(get_db)
):
    user_data = get_current_user(request)
    id_usuario = user_data["user_id"]

    nuevo_like = LikeService.dar_like(db, id_usuario, like.id_publicacion)
    
    if not nuevo_like:
        raise HTTPException(status_code=400, detail="El usuario ya dio like")
    
    return nuevo_like


@router.delete("/{id_publicacion}")
def quitar_like(
    id_publicacion: int, 
    request: Request,
    db: Session = Depends(get_db)
):
    user_data = get_current_user(request)
    id_usuario = user_data["user_id"]
    
    if not LikeService.quitar_like(db, id_usuario, id_publicacion):
        raise HTTPException(status_code=404, detail="Like no encontrado")
    
    return {"message": "Like eliminado"}

@router.get("/{id_publicacion}")
def obtener_likes(
    id_publicacion: int, 
    db: Session = Depends(get_db)
):
    return LikeService.obtener_likes_publicacion(db, id_publicacion)





@router.post("/comentar", response_model=ComentarioRespuesta)
def crear_comentario(
    comentario: Comment_Twatt, 
    request: Request,
    db: Session = Depends(get_db)
):
    user_data = get_current_user(request)
    id_usuario = user_data["user_id"]
    
    nuevo_comentario = CommentService.crear_comentario(
        db, 
        id_usuario, 
        comentario.id_publicacion, 
        comentario.contenido
    )
    
    return nuevo_comentario

@router.delete("/{id_comentario}")
def eliminar_comentario(
    id_comentario: int, 
    request: Request,
    db: Session = Depends(get_db)
):
    user_data = get_current_user(request)
    id_usuario = user_data["user_id"]
    
    if not CommentService.eliminar_comentario(db, id_comentario, id_usuario):
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    
    return {"message": "Comentario eliminado"}

@router.get("/{id_publicacion}")
def obtener_comentarios(
    id_publicacion: int, 
    db: Session = Depends(get_db)
):
    return CommentService.obtener_comentarios_publicacion(db, id_publicacion)