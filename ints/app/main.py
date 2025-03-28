from fastapi import FastAPI
import os

from modules.router_likes import router as r_likes
from modules.router_bookmarks import router as r_bookmarks
from shared.db.db_engine import init_db

VERSION = os.getenv("VERSION", "1.0.0")

app = FastAPI(
    title="Servicio de Interacciones",
    description="API para gestión de likes y comentarios",
    version=VERSION
)

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
async def api_welcome():
    return {"message": "Hello, bienvenido a twatter ints!"}

# Register your API routes
app.include_router(r_likes)
app.include_router(r_bookmarks)