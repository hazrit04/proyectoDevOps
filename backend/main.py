from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, tasks
from app import models
from app.database import engine

# Crear tablas (solo la primera vez o si no existen)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestión de Tareas",
    description="Proyecto Final - Infraestructura para el Desarrollo Continuo",
    version="1.0.0"
)

# Permitir acceso desde el frontend (ajusta el origen si es necesario)
origins = [
    "http://localhost:3000",  # para desarrollo local
    "https://<TU-STATIC-WEB-APP>.azurestaticapps.net"  # para producción en Azure
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
