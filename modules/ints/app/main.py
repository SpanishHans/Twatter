from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.rutas import interacciones  # Usar src. explícitamente
from src.config.database import engine
from src.modelos import modelos

# Crear tablas
modelos.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servicio de Interacciones",
    description="API para gestión de likes y comentarios",
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
app.include_router(interacciones.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Servicio de Interacciones activo"}

# Para ejecutar con un puerto específico
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)