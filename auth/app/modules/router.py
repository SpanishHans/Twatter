from fastapi import APIRouter, HTTPException, Depends
from fastapi import Response
from sqlalchemy.orm import Session

from modules.models import User_On_DB
from modules.db_engine import get_db
from modules.schemas import UsuarioNuevo, UsuarioLogin
from modules.auth_service import AuthService


router = APIRouter(tags=["Autenticación"])




@router.post("/registro")
def register(user_data: UsuarioNuevo, db: Session = Depends(get_db)):
    # Check if username or email already exists
    if db.query(User_On_DB).filter_by(nombre_usuario=user_data.nombre_usuario).first():
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    if db.query(User_On_DB).filter_by(correo=user_data.correo).first():
        raise HTTPException(status_code=400, detail="Correo ya usado")
    
    # Hash password
    hashed_password = AuthService.hash_password(user_data.contrasena.get_secret_value())

    # Create new user
    new_user = User_On_DB(
        nombre_usuario=user_data.nombre_usuario,
        correo=user_data.correo,
        contrasena_hash=hashed_password,
        foto_perfil=user_data.foto_perfil,
        biografia=user_data.biografia
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Registro correcto"}





@router.post("/login")
def login(user_data: UsuarioLogin, response: Response, db: Session = Depends(get_db)):
    # Get user by username
    user = db.query(User_On_DB).filter_by(nombre_usuario=user_data.nombre_usuario).first()
    
    if not user or not AuthService.verify_password(user_data.contrasena.get_secret_value(), user.contrasena_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token
    token = AuthService.generate_token(user.id, user.nombre_usuario)

    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # JavaScript can't access
        secure=False,  # Use only in HTTPS
        samesite="Lax",  # Helps prevent CSRF
        max_age=60 * 60 * 24  # 1-day expiration
    )

    return {"message": "Login correcto"}





@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Log out correcto"}
