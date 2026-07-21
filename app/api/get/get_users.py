from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.get_db import get_db
from app.crud.get.get_users import get_all_users_db
from app.middleware.current_user import get_current_user
from app.models.model_user import User

router = APIRouter()

@router.get("/users")
async def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ✅ CORREGIDO: Acceder como atributo de objeto, no como diccionario
    if current_user.type_user_id != 1 and not current_user.is_admin:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    response = get_all_users_db(db)
    if response:
        return {"message": response}
    else:
        return {"error": "Error al obtener los usuarios"}