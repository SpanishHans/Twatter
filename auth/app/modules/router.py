from fastapi import APIRouter, HTTPException, Depends
from fastapi import Response

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.user import User_on_db
from shared.db.db_engine import get_db

from modules.schemas import NewUser, UserLogin
from modules.auth_service import AuthService

router = APIRouter(tags=["Autenticación"])

@router.post("/registro")
async def register(
    user_api: NewUser,
    db: AsyncSession = Depends(get_db)):
    
    result_username = await db.execute(select(User_on_db).where(User_on_db.username == user_api.username))
    existing_user = result_username.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    result_email = await db.execute(select(User_on_db).where(User_on_db.email == user_api.email))
    existing_email = result_email.scalar_one_or_none()
    if existing_email:
        raise HTTPException(status_code=400, detail="Correo ya usado")
    
    hashed_password = AuthService.hash_password(user_api.password.get_secret_value())

    new_user = User_on_db(
        username=user_api.username,
        email=user_api.email,
        password_hash=hashed_password,
        profile_picture=user_api.profile_picture,
        biography=user_api.biography
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "Registro correcto"}





@router.post("/login")
async def login(
    user_api: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(User_on_db).where(User_on_db.username == user_api.username)
    )
    user = result.scalar_one_or_none()

    if not user or not AuthService.verify_password(user_api.password.get_secret_value(), user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = AuthService.generate_token(user.id, user.username)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # JavaScript can't access
        secure=False,  # Use only in HTTPS
        samesite="Lax",  # Helps prevent CSRF
        max_age=60 * 60 * 24  # 1-day expiration
    )

    return {"message": "Login correcto"}






from fastapi import Request
from fastapi.responses import JSONResponse

@router.get("/verify-token")
async def verify_token_endpoint(request: Request):
    token = AuthService.extract_token_from_request(request)
    user = AuthService.verify_token(token)
    return JSONResponse(content=user)





@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Log out correcto"}
