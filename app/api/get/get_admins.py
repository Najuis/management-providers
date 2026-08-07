from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.get_db import get_db
from app.crud.get.get_admins import get_all_admins_db
from app.middleware.current_user import get_current_user
from app.models.model_user import User

router = APIRouter()

@router.get("/admins")
async def get_all_admins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.type_user_id != 1 and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")

    response = get_all_admins_db(db)
    if response:
        return {"message": response}
    else:
        return {"error": "Error al obtener los administradores"}
