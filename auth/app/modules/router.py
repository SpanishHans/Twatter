import os
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError

from fastapi import APIRouter, HTTPException, Depends, Response, Request

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from shared.models.user import User_on_db
from shared.db.db_engine import get_db

from modules.schemas import RegisterUser, LoginUser
from modules.service_auth import AuthService

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")  # Same as in auth container
ALGORITHM = os.getenv("ALGORITHM", "HS256")

router = APIRouter(tags=["Autenticación"])

@router.post("/registro")
async def register(
    user_on_api: RegisterUser,
    db: AsyncSession = Depends(get_db)
):
    try:
        result_username = await db.execute(select(User_on_db).where(User_on_db.username == user_on_api.username))
        existing_user = result_username.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="Usuario ya existe")
    
        result_email = await db.execute(select(User_on_db).where(User_on_db.email == user_on_api.email))
        existing_email = result_email.scalar_one_or_none()
        if existing_email:
            raise HTTPException(status_code=400, detail="Correo ya usado")
        
        hashed_password = AuthService.hash_password(user_on_api.password.get_secret_value())
    
        new_user = User_on_db(
            username=user_on_api.username,
            email=user_on_api.email,
            password_hash=hashed_password,
            profile_picture=None,
            biography=None
        )
    
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    
        return {
            "message": "Registro correcto",
            "user_id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
        
    except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error occurred: {e}")





@router.post("/login")
async def login(
    user_on_api: LoginUser,
    response: Response,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User_on_db).where(User_on_db.username == user_on_api.username)
    )
    user = result.scalar_one_or_none()

    if not user or not AuthService.verify_password(user.password_hash, user_on_api.password.get_secret_value()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token, refresh_token = AuthService.generate_tokens(user.id, user.username)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # JavaScript can't access
        secure=False,  # Use only in HTTPS
        samesite="Lax",  # Helps prevent CSRF
        max_age=60 * 60 * 24 * 7  # 1-day expiration
    )

    return {"access_token": access_token, "token_type": "bearer", "message": "Login correcto"}





@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Log out correcto"}





@router.post("/reauth")
async def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("token_type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload["sub"]
        username = payload["username"]

        new_access_token, _ = AuthService.generate_tokens(user_id, username)

        return {"access_token": new_access_token, "token_type": "bearer"}

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
