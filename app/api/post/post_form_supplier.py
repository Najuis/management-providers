from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.get_db import get_db
from app.crud.post.post_form_supplier_db import post_form_supplier_db
from app.schemas.form_data import FormData
from app.middleware.current_user import get_current_user
from app.models.model_user import User

# ✅ Usamos 'routes' para que coincida con tu main.py actual
routes = APIRouter()

@routes.post("/form_supplier", status_code=status.HTTP_201_CREATED)
async def post_form_supplier(
    form_data: FormData,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id_user
    response = await post_form_supplier_db(db, form_data, user_id)
    
    if not response:
        # ✅ CORREGIDO: Lanzar excepción HTTP real en lugar de devolver un 200 OK con error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error interno al guardar el formulario de proveedor"
        )
        
    return {"message": response}