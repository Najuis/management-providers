from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.database.core import create_tables

# Cargar variables de entorno
load_dotenv()

app = FastAPI()

# Configuración CORS corregida
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.api.post.post_login import router as login

app.include_router(login, prefix="/api")

# Montar archivos estáticos
app.mount("/pages", StaticFiles(directory="app/pages"), name="pages")

@app.get("/")
async def root():
    return FileResponse("app/pages/login/login.html")
