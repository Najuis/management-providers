from pydantic import BaseModel, EmailStr
from typing import Optional, List

class FormData(BaseModel):
    email: EmailStr
    password: str
    type_user_id: int
    identification_type_id: Optional[int] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    document: Optional[str] = None
    address: Optional[str] = None
    region_id: Optional[int] = None
    city_id: Optional[int] = None
    country_id: Optional[int] = None
    office_id: Optional[int] = None

    #NaturalPersonSchema
    date_expedition: Optional[str] = None
    date_birth: Optional[str] = None
    zone: Optional[str] = None
    employee: Optional[str] = None
    number_nit: Optional[str] = None
    charge: Optional[str] = None
    monthly_income: Optional[float] = None
    other_income: Optional[float] = None

    #LegalEntitiesSchema
    name_society_social: Optional[str] = None
    number_nit: Optional[str] = None
    society_type: Optional[str] = None
    type_bonding: Optional[str] = None

    #TaxFiscalInformationSchema
    common: Optional[bool] = None
    big_taxpayer: Optional[bool] = None
    simplified_regime: Optional[bool] = None
    resolution_number: Optional[str] = None
    date_resolution: Optional[str] = None

    #FinancialInformationSchema
    total_active: Optional[float] = None
    total_passive: Optional[float] = None
    total_equity: Optional[float] = None
    heritage: Optional[float] = None
    monthly_expenditure: Optional[float] = None
    monthly_income: Optional[float] = None

    #LegalRepresentativeSchema
    name_legal_representative: Optional[str] = None
    number_document: Optional[str] = None
    city_id: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

    #ReferenceSchema
    company_or_bank_name: Optional[str] = None
    holder_name: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    account_type: Optional[str] = None
    social_reason: Optional[str] = None

    #ShareCompositionSchema
    type_identification: Optional[str] = None
    number_identification: Optional[str] = None
    social_reason: Optional[str] = None
    name_complete: Optional[str] = None
    porcentage_porcentage: Optional[float] = None

    #OccupationalHealthSafetySchema
    document: Optional[str] = None
    fulfilled: Optional[bool] = False
    observation: Optional[str] = None

    #HealthSafetySchema
    document: Optional[str] = None
    fulfilled: Optional[bool] = False
    observation: Optional[str] = None

    #RequiredDocumentSchema
    document_name: str
    is_verified: Optional[bool] = False
