from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import DATABASE_URL
from app.database.base import Base
from app.models import (
    User, City, Country, FinancialInformation, HealthSafetyRequirements,
    InfoShareComposition, LegalRepresentativeInformation, NaturalPerson,
    LegalPerson, OccupationalHealthSafetyRequirements, Office,
    RequiredDocuments, References, TypeUser, TypeDocument, Region,
    TaxFiscalInformation, GeneralInformation, Municipality,
    AuthorizationsPolicies,
    # ✅ NUEVO: Modelos de Fase 4 (Submissions)
    Submission, SubmissionDocument, AuditLog
)

# ============================================
# CONFIGURACIÓN DEL ENGINE
# ============================================
# Soporte para SQLite (desarrollo) y PostgreSQL (producción)
connect_args = {}
if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False  # Cambiar a True para ver queries SQL en consola
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# ============================================
# LISTA DE TABLAS A CREAR
# ============================================
tables = [
    User.__table__,
    TypeUser.__table__,
    Office.__table__,
    City.__table__,
    Region.__table__,
    TaxFiscalInformation.__table__,
    FinancialInformation.__table__,
    HealthSafetyRequirements.__table__,
    InfoShareComposition.__table__,
    LegalRepresentativeInformation.__table__,
    NaturalPerson.__table__,
    LegalPerson.__table__,
    OccupationalHealthSafetyRequirements.__table__,
    RequiredDocuments.__table__,
    References.__table__,
    TypeDocument.__table__,
    Country.__table__,
    GeneralInformation.__table__,
    Municipality.__table__,
    AuthorizationsPolicies.__table__,
    # ✅ NUEVO: Tablas de Fase 4 (Submissions)
    Submission.__table__,
    SubmissionDocument.__table__,
    AuditLog.__table__,
]

# ============================================
# FUNCIÓN PARA CREAR/ACTUALIZAR TABLAS
# ============================================
def create_tables():
    """Crear todas las tablas en la base de datos"""
    try:
        Base.metadata.create_all(bind=engine, tables=tables)
        db_type = DATABASE_URL.split(':')[0].upper() if DATABASE_URL else "UNKNOWN"
        print(f"✅ Database create or update - {db_type}")
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        raise