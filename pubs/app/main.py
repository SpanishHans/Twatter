from fastapi import FastAPI
import os

from modules.router import router

VERSION = os.getenv("VERSION", "1.0.0")

app = FastAPI(
    title="Servicio de Publicaciones",
    description="API para gestión de publicaciones",
    version=VERSION
)

# Incluir rutas
app.include_router(router)