from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .rutas import usuarios
from .config.database import engine
from .modelos import modelos

# Crear tablas
modelos.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servicio de Autenticación",
    description="API para gestión de usuarios y autenticación",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(usuarios.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Servicio de Autenticación activo"}