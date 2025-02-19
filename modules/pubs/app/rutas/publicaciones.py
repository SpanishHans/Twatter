from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
import requests

from ..config.database import get_db
from ..servicios.publicacion_service import PublicacionService
from ..esquemas.publicacion import PublicacionCrear, PublicacionRespuesta

router = APIRouter(prefix="/publicaciones", tags=["Publicaciones"])

@router.post("/", response_model=PublicacionRespuesta)
def crear_publicacion(
    publicacion: PublicacionCrear, 
    token: str = Header(...),  # Token en el header
    db: Session = Depends(get_db)
):
    # Validar token con servicio de autenticación
    try:
        # Validar token en el puerto 8000
        respuesta_auth = requests.post(
            "http://localhost:8000/api/v1/auth/validar-token", 
            json={"token": token}
        )
        
        if respuesta_auth.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        datos_token = respuesta_auth.json()
        usuario = datos_token.get("usuario")
        
        # Obtener información del usuario desde el servicio de autenticación
        respuesta_usuario = requests.post(
            "http://localhost:8000/api/v1/auth/usuarios", 
            json={"nombre_usuario": usuario}
        )
        
        if respuesta_usuario.status_code != 200:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        usuario_data = respuesta_usuario.json()[0]
        id_usuario = usuario_data['id']
        
        # Crear publicación
        nueva_publicacion = PublicacionService.crear_publicacion(
            db=db, 
            id_usuario=id_usuario,
            contenido=publicacion.contenido,
            es_recomparte=publicacion.es_recomparte or False,
            id_publicacion_original=publicacion.id_publicacion_original,
            archivos_multimedia=[
                {"tipo_medio": archivo.tipo_medio, "url_medio": archivo.url_medio} 
                for archivo in (publicacion.archivos_multimedia or [])
            ]
        )
        
        return nueva_publicacion
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[PublicacionRespuesta])
def obtener_publicaciones(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return PublicacionService.obtener_publicaciones(db, skip, limit)

@router.get("/{publicacion_id}", response_model=PublicacionRespuesta)
def obtener_publicacion(
    publicacion_id: int, 
    db: Session = Depends(get_db)
):
    return PublicacionService.obtener_publicacion_por_id(db, publicacion_id)

@router.delete("/{publicacion_id}")
def eliminar_publicacion(
    publicacion_id: int, 
    token: str = Header(...), 
    db: Session = Depends(get_db)
):
    # Validar token con servicio de autenticación
    try:
        # Validar token en el puerto 8000
        respuesta_auth = requests.post(
            "http://localhost:8000/api/v1/auth/validar-token", 
            json={"token": token}
        )
        
        if respuesta_auth.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        datos_token = respuesta_auth.json()
        usuario = datos_token.get("usuario")
        
        # Obtener información del usuario desde el servicio de autenticación
        respuesta_usuario = requests.post(
            "http://localhost:8000/api/v1/auth/usuarios", 
            json={"nombre_usuario": usuario}
        )
        
        if respuesta_usuario.status_code != 200:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        usuario_data = respuesta_usuario.json()[0]
        id_usuario = usuario_data['id']
        
        # Eliminar publicación
        PublicacionService.eliminar_publicacion(db, publicacion_id, id_usuario)
        
        return {"message": "Publicación eliminada exitosamente"}
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))