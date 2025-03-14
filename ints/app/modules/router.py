from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

import requests

from modules.db_engine import get_db
from modules.schema_like import LikeService
from modules.schema_comm import ComentarioService
from modules.schema_api import LikeTwatt, Comment_Twatt, LikeRespuesta, ComentarioRespuesta

router = APIRouter(tags=["Interacciones"])

def validar_token_y_obtener_usuario(token: str):
    # Validar token con servicio de autenticación
    respuesta_auth = requests.post(
        "http://localhost:8000/api/v1/auth/validar-token", 
        json={"token": token}
    )
    
    if respuesta_auth.status_code != 200:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    datos_token = respuesta_auth.json()
    usuario = datos_token.get("usuario")
    
    # Obtener información del usuario
    respuesta_usuario = requests.post(
        "http://localhost:8000/api/v1/auth/usuarios", 
        json={"nombre_usuario": usuario}
    )
    
    if respuesta_usuario.status_code != 200:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario_data = respuesta_usuario.json()[0]
    return usuario_data['id']





@router.post("/like", response_model=LikeRespuesta)
def dar_like(
    like: LikeTwatt, 
    token: str = Header(...), 
    db: Session = Depends(get_db)
):
    id_usuario = validar_token_y_obtener_usuario(token)
    
    nuevo_like = LikeService.dar_like(db, id_usuario, like.id_publicacion)
    
    if not nuevo_like:
        raise HTTPException(status_code=400, detail="El usuario ya dió like")
    
    return nuevo_like

@router.delete("/{id_publicacion}")
def quitar_like(
    id_publicacion: int, 
    token: str = Header(...), 
    db: Session = Depends(get_db)
):
    id_usuario = validar_token_y_obtener_usuario(token)
    
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
    token: str = Header(...), 
    db: Session = Depends(get_db)
):
    id_usuario = validar_token_y_obtener_usuario(token)
    
    nuevo_comentario = ComentarioService.crear_comentario(
        db, 
        id_usuario, 
        comentario.id_publicacion, 
        comentario.contenido
    )
    
    return nuevo_comentario

@router.delete("/{id_comentario}")
def eliminar_comentario(
    id_comentario: int, 
    token: str = Header(...), 
    db: Session = Depends(get_db)
):
    id_usuario = validar_token_y_obtener_usuario(token)
    
    if not ComentarioService.eliminar_comentario(db, id_comentario, id_usuario):
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    
    return {"message": "Comentario eliminado"}

@router.get("/{id_publicacion}")
def obtener_comentarios(
    id_publicacion: int, 
    db: Session = Depends(get_db)
):
    return ComentarioService.obtener_comentarios_publicacion(db, id_publicacion)