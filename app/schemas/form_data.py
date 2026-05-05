from pydantic import BaseModel, EmailStr
from typing import Optional


class FormData(BaseModel):
    email: EmailStr
    type_user_id: int

    # General Information
    date_information: Optional[str] = None
    city_id: Optional[int] = None
    office_id: Optional[int] = None

    # Natural Person
    identification_type_id: Optional[int] = None
    municipality_id: Optional[int] = None
    region_id: Optional[int] = None
    country_id: Optional[int] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    document: Optional[str] = None
    expedition_date: Optional[str] = None
    birth_date: Optional[str] = None
    address: Optional[str] = None
    zone: Optional[str] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    nit: Optional[str] = None
    occupation: Optional[str] = None
    monthly_income: Optional[float] = None
    other_income: Optional[float] = None
    specify: Optional[str] = None

    # Legal Person
    reason_or_name: Optional[str] = None
    society_type: Optional[str] = None
    link_type: Optional[str] = None

    # Tax Fiscal Information
    common: Optional[bool] = None
    big_taxpayer: Optional[bool] = None
    simplified_regime: Optional[bool] = None
    self_retained_resolution: Optional[str] = None
    self_retained_date: Optional[str] = None
    big_taxpayer_resolution: Optional[str] = None
    big_taxpayer_date: Optional[str] = None
    self_retained_ica_resolution: Optional[str] = None
    self_retained_ica_date: Optional[str] = None

    # Financial Information
    total_active: Optional[float] = None
    total_passive: Optional[float] = None
    patrimony: Optional[float] = None
    monthly_expenditure: Optional[float] = None

    # Legal Representative Information
    rep_name: Optional[str] = None
    rep_last_name: Optional[str] = None
    rep_document: Optional[str] = None
    rep_city_id: Optional[int] = None
    rep_phone: Optional[str] = None
    rep_email: Optional[EmailStr] = None

    # References
    bank_name: Optional[str] = None
    titular_name: Optional[str] = None
    ref_phone: Optional[str] = None
    ref_address: Optional[str] = None
    account_type: Optional[str] = None
    ref_social_reason: Optional[str] = None

    # Share Composition
    identification_type: Optional[str] = None
    numero_identification: Optional[str] = None
    share_social_reason: Optional[str] = None
    full_name: Optional[str] = None
    percentage: Optional[float] = None

    # Occupational Health & Safety Requirements
    ohs_document: Optional[str] = None
    ohs_fulfilled: Optional[bool] = False
    ohs_observation: Optional[str] = None

    # Health Safety Requirements
    hs_document: Optional[str] = None
    hs_fulfilled: Optional[bool] = False
    hs_observation: Optional[str] = None

    # Required Documents
    document_name: Optional[str] = None
    is_verified: Optional[bool] = False

    # Authorizations & Policies
    auth_document_number: Optional[str] = None
    auth_expedition_place: Optional[str] = None
    auth_acting_as: Optional[str] = None
    auth_ciiu_code: Optional[str] = None
    auth_economic_activity: Optional[str] = None
    auth_licit_origin: Optional[bool] = False
    auth_knowledge_normativity: Optional[bool] = False
    auth_no_third_party_deposits: Optional[bool] = False
    auth_reality_statement: Optional[bool] = False
    auth_sagrilat_verification: Optional[bool] = False
    auth_public_resources: Optional[bool] = False
    auth_public_power: Optional[bool] = False
    auth_public_recognition: Optional[bool] = False
    auth_pep_link: Optional[bool] = False
    auth_pep_position: Optional[str] = None
    auth_pep_link_date: Optional[str] = None
    auth_authorize_restrictive_lists: Optional[bool] = False
    auth_policy_adherence: Optional[bool] = False
