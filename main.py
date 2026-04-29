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
from app.api.get.get_users import routes as users
from app.api.get.get_city import routes as city
from app.api.get.get_country import routes as country
from app.api.get.get_office import routes as office
from app.api.get.get_user_id import routes as userbyid  

app.include_router(login, prefix="/api")
app.include_router(info_user, prefix="/api/admin")
app.include_router(users, prefix="/api/admin")
app.include_router(city, prefix="/api")
app.include_router(country, prefix="/api")
app.include_router(office, prefix="/api")
app.include_router(userbyid, prefix="/api/admin")

# Montar archivos estáticos
app.mount("/pages", StaticFiles(directory="app/pages"), name="pages")

@app.get("/")
async def root():
    return FileResponse("app/pages/login/login.html")

@app.get("/admin/dashboard")
async def dashboard():
    return FileResponse("app/pages/admin/dashboard/dashboard.html")

@app.get("/admin/formulario")
async def formulario_page():
    return FileResponse("app/pages/formulario/formulario.html")

@app.get("/admin/confirmacion")
async def confirmacion_page():
    return FileResponse("app/pages/confirmacion/confirmacion.html")

@app.get("/admin/validation")
async def admin_validation():
    return FileResponse("app/pages/admin/validation/validation.html")