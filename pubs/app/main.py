from fastapi import FastAPI
import os

from modules.router import router
from shared.db.db_engine import init_db

VERSION = os.getenv("VERSION", "1.0.0")

app = FastAPI(
    title="Servicio de Publicaciones",
    description="API para gestión de publicaciones",
    version=VERSION
)

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
async def api_welcome():
    return {"message": "Hello, bienvenido a twatter pubs!"}

# Register your API routes
app.include_router(router)
