from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.get_db import get_db
from app.crud.post.post_form_supplier_db import post_form_supplier_db
from app.schemas.form_data import FormData

routes = APIRouter()

@routes.post("/form_supplier")
async def post_form_supplier(
    form_data: FormData,
    db: Session = Depends(get_db)
):
    response = await post_form_supplier_db(db, form_data)
    if response:
        return {"message": response}    
    else:
        return {"error": "Error al guardar el formulario de proveedor"} 