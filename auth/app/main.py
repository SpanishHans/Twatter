from fastapi import FastAPI
import os

from modules.router import router
from shared.db.db_engine import init_db
from shared.middleware.csp import CSPMiddleware

VERSION = os.getenv("VERSION", "1.0.0")

app = FastAPI(
    title="Servicio de Autenticación",
    description="API para gestión de usuarios y autenticación",
    version=VERSION
)
# app.add_middleware(CSPMiddleware)

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
async def read_root():
    return {"message": "Hello, bienvenido a twatter auth!"}

# Register your API routes
app.include_router(router)
