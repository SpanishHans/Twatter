from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# from typing import List

from modules.db_engine import get_db
from modules.schema_db import User_template
from modules.schema_api import UsuarioNuevo, UsuarioLogin, Token
from modules.schema_auth import AuthService

router = APIRouter(tags=["Autenticación"])

@router.post("/registro", response_model=Token)
def registrar_usuario(usuario: UsuarioNuevo, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    usuario_existente = db.query(User_template).filter(
        (User_template.nombre_usuario == usuario.nombre_usuario) |
        (User_template.correo == usuario.correo)
    ).first()

    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    # Hashear contraseña
    hashed_password = AuthService.crear_hash_contrasena(usuario.contrasena.get_secret_value())

    # Crear nuevo usuario
    nuevo_usuario = User_template(
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
def login(datos_login: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = AuthService.autenticar_usuario(db, datos_login.nombre_usuario, datos_login.contrasena.get_secret_value())
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    access_token = AuthService.crear_token_acceso(
        data={"sub": usuario.nombre_usuario}
    )

    return {"token_access": access_token, "token_type": "bearer"}






# @router.post("/validar-token")
# def validar_token(token: dict):
#     payload = AuthService.verificar_token(token["token"])
#     if not payload:
#         raise HTTPException(status_code=401, detail="Token inválido")
#     return {"valido": True, "usuario": payload.get("sub")}






# @router.post("/usuarios", response_model=List[UsuarioRespuesta])
# def buscar_usuarios(
#     busqueda: UsuarioBusqueda,
#     db: Session = Depends(get_db)
# ):
#     if busqueda.nombre_usuario:
#         usuario = db.query(User_template).filter(User_template.nombre_usuario == busqueda.nombre_usuario).first()
#         if usuario:
#             return [usuario]
#         return []
#     return db.query(User_template).offset(busqueda.skip).limit(busqueda.limit).all()
