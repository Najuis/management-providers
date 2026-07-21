from fastapi import Depends, APIRouter, HTTPException
from app.schemas.info_user import InfoUser
from app.crud.post.post_user import post_user
from app.database.get_db import get_db
from sqlalchemy.orm import Session
from app.middleware.current_user import get_current_user

router = APIRouter()

@router.post("/user")
async def info_user(
    user_info: InfoUser,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Verificar que solo los admins puedan crear usuarios
    if not current_user.is_admin: 
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")
    
    resultado = await post_user(user_info, db)
    
    if "successfully" in resultado["message"]:
        return {"message": "Usuario creado exitosamente", "success": True}
    else:
        raise HTTPException(status_code=400, detail=resultado["message"])