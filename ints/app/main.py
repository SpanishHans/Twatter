from fastapi import FastAPI
import os

from modules.router import router

VERSION = os.getenv("VERSION", "1.0.0")

app = FastAPI(
    title="Servicio de Interacciones",
    description="API para gestión de likes y comentarios",
    version=VERSION
)

# Incluir rutas
app.include_router(router)
