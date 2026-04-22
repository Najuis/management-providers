from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import DATABASE_URL
from app.database.base import Base
from app.models import User, City, Country, FinancialInformation, HealthSafetyRequirements, InfoShareComposition, LegalRepresentativeInformation, NaturalPerson, LegalEntities, OccupationalHealthSafetyRequirements, Regime, Office, RequiredDocuments, References, TypeUser, TypeDocument, Region, TaxFiscalInformation

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

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
    LegalEntities.__table__,
    OccupationalHealthSafetyRequirements.__table__,
    Regime.__table__,
    RequiredDocuments.__table__,
    References.__table__,
    TypeDocument.__table__,
    Country.__table__,
]

def create_tables():
    Base.metadata.create_all(bind=engine, tables=tables)
    print("Database create or update")