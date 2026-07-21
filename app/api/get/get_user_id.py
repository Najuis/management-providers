from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.get_db import get_db
from app.crud.get.get_user_id import get_user_id_db
from app.middleware.current_user import get_current_user
from app.models.model_user import User

router = APIRouter()

@router.get("/userbyid")
async def get_user_id(
    id_user: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ✅ CORREGIDO: Acceder como atributo de objeto, no como diccionario
    if current_user.type_user_id != 1 and not current_user.is_admin:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    response = await get_user_id_db(db, id_user)
    return {"message": response}