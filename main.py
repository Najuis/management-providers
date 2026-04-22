from fastapi import FastAPI
from dotenv import load_dotenv
from app.database.core import create_tables
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from fastapi.middleware.cors import CORSMiddleware
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

from app.api.post.post_login import router as login
from app.api.post.post_user import router as info_user

app.include_router(login, prefix="/api")
app.include_router(info_user, prefix="/api")

# Montar archivos estáticos
app.mount("/pages", StaticFiles(directory="app/pages"), name="pages")

@app.get("/")
async def root():
    return FileResponse("app/pages/login/login.html")

@app.get("/admin/dashboard")
async def dashboard():
    return FileResponse("app/pages/admin/dashboard/dashboard.html")