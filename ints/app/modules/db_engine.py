from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear motor de base de datos
engine = create_engine(DATABASE_URL)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
