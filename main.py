from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.database.core import create_tables

# Cargar variables de entorno
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se ejecuta al iniciar el servidor
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Configuración CORS corregida
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# from app.api.post.login import router as login
# app.include_router(login, prefix="/api")