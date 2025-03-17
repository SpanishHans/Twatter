from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
import requests

from shared.db.db_engine import get_db
from shared.auth.auth import get_current_user

from modules.twatt_service import TwattService
from modules.schemas import PublicacionCrear, PublicacionRespuesta

router = APIRouter(tags=["Publicaciones"])

@router.post("/twatt", response_model=PublicacionRespuesta)
def crear_twatt(
        publicacion: PublicacionCrear,
        request: Request,
        db: Session = Depends(get_db)
    ):

    # Validar token con servicio de autenticación
    try:
        # Validar token en el puerto 8000
        user_data = get_current_user(request)
        id_usuario = user_data["user_id"]

        # Crear publicación
        nueva_publicacion = TwattService.crear_publicacion(
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

@router.get("/twatts", response_model=List[PublicacionRespuesta])
def obtener_twatts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return TwattService.obtener_publicaciones(db, skip, limit)

@router.get("/{publicacion_id}", response_model=PublicacionRespuesta)
def obtener_twatt(
    publicacion_id: int,
    db: Session = Depends(get_db)
):
    return TwattService.obtener_publicacion_por_id(db, publicacion_id)

@router.delete("/{publicacion_id}")
def eliminar_twatt(
    publicacion_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    # Validar token con servicio de autenticación
    try:
        # Validar token en el puerto 8000
        user_data = get_current_user(request)
        id_usuario = user_data["user_id"]

        # Eliminar publicación
        TwattService.eliminar_publicacion(db, publicacion_id, id_usuario)

        return {"message": "Publicación eliminada exitosamente"}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))