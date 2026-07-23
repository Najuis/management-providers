# app/database/core.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Importar Base desde el archivo separado (EVITA CICLOS)
from app.database.base import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./management_providers.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Crear todas las tablas en la base de datos"""
    # Importar modelos aquí para evitar ciclos
    from app.models import User, City, Country, Office, TypeUser, TypeDocument, Region, Municipality
    from app.models import NaturalPerson, LegalPerson, LegalRepresentativeInformation, InfoShareComposition
    from app.models import TaxFiscalInformation, FinancialInformation, References
    from app.models import OccupationalHealthSafetyRequirements, HealthSafetyRequirements
    from app.models import AuthorizationsPolicies, RequiredDocuments
    from app.models.submission_models import Submission, SubmissionDocument
    
    Base.metadata.create_all(bind=engine)
    print("✅ Database create or update - SQLITE")

def get_db():
    """Obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()