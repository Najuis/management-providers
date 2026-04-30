from sqlalchemy.orm import Session
from app.models.model_user import User
from app.models.model_type_user import TypeUser
from app.models.model_type_document import TypeDocument
from app.models.model_financial_information import FinancialInformation
from fastapi import HTTPException

async def post_form_supplier_db(db: Session, form_data: dict):

    return form_data