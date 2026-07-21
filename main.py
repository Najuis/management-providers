from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database.get_db import get_db
from app.middleware.current_user import get_current_user

# 1. Cargar variables de entorno
load_dotenv()

# 2. ✅ IMPORTANTE: Importar TODOS los modelos ANTES de create_tables()
from app.models import (
    User, City, Country, FinancialInformation, HealthSafetyRequirements,
    InfoShareComposition, LegalRepresentativeInformation, NaturalPerson,
    LegalPerson, OccupationalHealthSafetyRequirements, Office,
    RequiredDocuments, References, TypeUser, TypeDocument, Region,
    TaxFiscalInformation, GeneralInformation, Municipality, AuthorizationsPolicies,
    Submission, SubmissionDocument, AuditLog
)
from app.database.core import create_tables

# 3. Crear tablas en la base de datos
create_tables()

# 4. Inicializar la aplicación FastAPI (¡ESTO DEBE IR ANTES DE LOS @app.get!)
app = FastAPI(title="Management Providers API", version="1.0.0")

# ============================================
# ✅ STATIC FILES - MOVIDO AQUÍ ARRIBA (DESPUÉS DE CREAR APP)
# ============================================
app.mount("/pages", StaticFiles(directory="app/pages"), name="pages")

# ============================================
# CORS
# ============================================
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# ROUTERS - POST
# ============================================
from app.api.post.post_login import router as login
from app.api.post.post_user import router as info_user
from app.api.post.post_form_supplier import routes as form_supplier
from app.api.post.upload_validation.router import router as submissions_router

# ============================================
# ROUTERS - GET
# ============================================
from app.api.get.get_users import router as users
from app.api.get.get_city import router as city
from app.api.get.get_country import router as country
from app.api.get.get_office import router as office
from app.api.get.get_user_id import router as userbyid

# ============================================
# INCLUIR ROUTERS
# ============================================
app.include_router(login, prefix="/api")
app.include_router(info_user, prefix="/api/admin")
app.include_router(form_supplier, prefix="/api")
app.include_router(submissions_router, prefix="/api/submissions", tags=["Submissions"])
app.include_router(users, prefix="/api/admin")
app.include_router(city, prefix="/api")
app.include_router(country, prefix="/api")
app.include_router(office, prefix="/api")
app.include_router(userbyid, prefix="/api/admin")

# ============================================
# ENDPOINTS ADICIONALES (compatibilidad frontend) - ✅ CORREGIDOS
# ============================================
@app.get("/api/cities")
async def get_cities(db: Session = Depends(get_db)):
    """Alias plural para /api/city"""
    from app.crud.get.get_city import get_city_db
    try:
        cities = await get_city_db(db)
        return cities if cities else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ciudades: {str(e)}")

@app.get("/api/countries")
async def get_countries(db: Session = Depends(get_db)):
    """Alias plural para /api/country"""
    from app.crud.get.get_country import get_country_db
    try:
        countries = await get_country_db(db)
        return countries if countries else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener países: {str(e)}")

@app.get("/api/offices")
async def get_offices(db: Session = Depends(get_db)):
    """Alias plural para /api/office"""
    from app.crud.get.get_office import get_office_db
    try:
        offices = await get_office_db(db)
        return offices if offices else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener oficinas: {str(e)}")

@app.get("/api/ciiu")
async def get_ciiu():
    """Códigos CIIU de ejemplo"""
    return [
        {"codigo": "0111", "descripcion": "Cultivo de cereales (excepto arroz), legumbres y semillas oleaginosas"},
        {"codigo": "0112", "descripcion": "Cultivo de arroz"},
        {"codigo": "1011", "descripcion": "Procesamiento y conservación de carne y productos cárnicos"},
        {"codigo": "4711", "descripcion": "Comercio al por menor en establecimientos no especializados"},
        {"codigo": "4661", "descripcion": "Comercio al por mayor de combustibles sólidos, líquidos y gaseosos"},
        {"codigo": "5210", "descripcion": "Almacenamiento y depósito"},
        {"codigo": "7010", "descripcion": "Actividades de consultoría de gestión"},
    ]

# ============================================
# ENDPOINT PERFIL DE USUARIO
# ============================================
@app.get("/api/user/profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Obtener perfil del usuario autenticado"""
    return {
        "id_user": current_user.id_user,
        "email": current_user.email,
        "name": current_user.email.split('@')[0],
        "type_user_id": current_user.type_user_id,
        "is_admin": current_user.is_admin,
        "is_active": current_user.is_active
    }

# ============================================
# RUTAS DE PÁGINAS HTML
# ============================================
@app.get("/")
async def root():
    return FileResponse("app/pages/login/login.html")

@app.get("/login")
async def login_page():
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

@app.get("/admin/validacion-documentos")
async def validacion_documentos_page():
    """Página de validación de documentos (Fase 4)"""
    return FileResponse("app/pages/admin/validacion_documentos/index.html")

@app.get("/usuario")
async def usuario_page():
    return FileResponse("app/pages/usuario/usuario.html")