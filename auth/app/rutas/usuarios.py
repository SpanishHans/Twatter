from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from conf.database import get_db
from modelos.modelos import Usuario
from esquemas.usuario import UsuarioCrear, UsuarioRespuesta
from esquemas.auth import Token, Login
from servicios.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class UsuarioBusqueda(BaseModel):
    nombre_usuario: Optional[str] = None
    skip: int = 0
    limit: int = 100

@router.post("/registro", response_model=Token)
def registrar_usuario(usuario: UsuarioCrear, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    usuario_existente = db.query(Usuario).filter(
        (Usuario.nombre_usuario == usuario.nombre_usuario) | 
        (Usuario.correo == usuario.correo)
    ).first()
    
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    
    # Hashear contraseña
    hashed_password = AuthService.crear_hash_contrasena(usuario.contrasena)
    
    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        nombre_usuario=usuario.nombre_usuario,
        correo=usuario.correo,
        contrasena_hash=hashed_password,
        foto_perfil=usuario.foto_perfil,
        biografia=usuario.biografia
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    # Generar token
    access_token = AuthService.crear_token_acceso(
        data={"sub": nuevo_usuario.nombre_usuario}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(datos_login: Login, db: Session = Depends(get_db)):
    usuario = AuthService.autenticar_usuario(db, datos_login.username, datos_login.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    access_token = AuthService.crear_token_acceso(
        data={"sub": usuario.nombre_usuario}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/validar-token")
def validar_token(token: dict):
    payload = AuthService.verificar_token(token["token"])
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    return {"valido": True, "usuario": payload.get("sub")}

@router.post("/usuarios", response_model=List[UsuarioRespuesta])
def buscar_usuarios(
    busqueda: UsuarioBusqueda, 
    db: Session = Depends(get_db)
):
    if busqueda.nombre_usuario:
        usuario = db.query(Usuario).filter(Usuario.nombre_usuario == busqueda.nombre_usuario).first()
        if usuario:
            return [usuario]
        return []
    return db.query(Usuario).offset(busqueda.skip).limit(busqueda.limit).all()