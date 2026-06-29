from fastapi import FastAPI
from dotenv import load_dotenv
from app.database.core import create_tables
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
create_tables()

app = FastAPI()

# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers existentes
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

# Static files
app.mount("/pages", StaticFiles(directory="app/pages"), name="pages")

# Rutas de páginas
@app.get("/")
async def root():
    return FileResponse("app/pages/login/login.html")

@app.get("/admin/dashboard")
async def dashboard():
    return FileResponse("app/pages/admin/dashboard/dashboard.html")

@app.get("/admin/formulario")
async def formulario_page():
    return FileResponse("app/pages/Formulario/formulario.html")

@app.get("/admin/confirmacion")
async def confirmacion_page():
    return FileResponse("app/pages/admin/confirmation/confirmation.html")

@app.get("/admin/validation")
async def admin_validation():
    return FileResponse("app/pages/admin/validation/validation.html")

@app.get("/customer/dashboard")
async def customer_dashboard():
    return FileResponse("app/pages/customer/dashboard.html")

@app.get("/admin/menu")
async def admin_menu_page():
    return FileResponse("app/pages/menu-admin/admin_menu.html")

@app.get("/usuario")
async def usuario_page():
    return FileResponse("app/pages/usuario/usuario.html")