from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
import requests

from conf.database import get_db
from servicios.like_service import LikeService
from servicios.comentario_service import ComentarioService
from esquemas.interacciones import LikeCrear, LikeRespuesta, ComentarioCrear, ComentarioRespuesta

router = APIRouter(prefix="/interacciones", tags=["Interacciones"])

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

@router.post("/likes", response_model=LikeRespuesta)
def dar_like(
    like: LikeCrear, 
    token: str = Header(...), 
    db: Session = Depends(get_db)
):
    id_usuario = validar_token_y_obtener_usuario(token)
    
    nuevo_like = LikeService.dar_like(db, id_usuario, like.id_publicacion)
    
    if not nuevo_like:
        raise HTTPException(status_code=400, detail="Like ya existe")
    
    return nuevo_like

@router.delete("/likes/{id_publicacion}")
def quitar_like(
    id_publicacion: int, 
    token: str = Header(...), 
    db: Session = Depends(get_db)
):
    id_usuario = validar_token_y_obtener_usuario(token)
    
    if not LikeService.quitar_like(db, id_usuario, id_publicacion):
        raise HTTPException(status_code=404, detail="Like no encontrado")
    
    return {"message": "Like eliminado"}

@router.get("/likes/{id_publicacion}")
def obtener_likes(
    id_publicacion: int, 
    db: Session = Depends(get_db)
):
    return LikeService.obtener_likes_publicacion(db, id_publicacion)

@router.post("/comentarios", response_model=ComentarioRespuesta)
def crear_comentario(
    comentario: ComentarioCrear, 
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

@router.delete("/comentarios/{id_comentario}")
def eliminar_comentario(
    id_comentario: int, 
    token: str = Header(...), 
    db: Session = Depends(get_db)
):
    id_usuario = validar_token_y_obtener_usuario(token)
    
    if not ComentarioService.eliminar_comentario(db, id_comentario, id_usuario):
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    
    return {"message": "Comentario eliminado"}

@router.get("/comentarios/{id_publicacion}")
def obtener_comentarios(
    id_publicacion: int, 
    db: Session = Depends(get_db)
):
    return ComentarioService.obtener_comentarios_publicacion(db, id_publicacion)