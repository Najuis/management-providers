from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.get_db import get_db
from app.middleware.current_user import get_current_user
from app.middleware.hasher import hasher
from app.models.model_user import User

router = APIRouter()


class UserStateUpdate(BaseModel):
    is_active: bool


class UserPasswordUpdate(BaseModel):
    password: str


class UserPermissionsUpdate(BaseModel):
    type_user_id: int
    is_admin: bool


@router.put("/user/{user_id}/state")
async def update_user_state(
    user_id: int,
    body: UserStateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and current_user.type_user_id != 1:
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")

    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not body.is_active and user.type_user_id == 1:
        admins_activos = db.query(User).filter(
            User.type_user_id == 1,
            User.is_active == True
        ).count()
        if admins_activos <= 1:
            raise HTTPException(status_code=400, detail="No se puede desactivar el último administrador activo")

    user.is_active = body.is_active
    db.commit()
    return {"message": "Usuario activado" if body.is_active else "Usuario desactivado", "id_user": user_id}


@router.put("/user/{user_id}/password")
async def reset_user_password(
    user_id: int,
    body: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and current_user.type_user_id != 1:
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")

    password = body.password
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 8 caracteres")
    if not any(c.isupper() for c in password):
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos una mayúscula")
    if not any(c.isdigit() for c in password):
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos un número")

    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.password = hasher(password)
    db.commit()
    return {"message": "Contraseña actualizada exitosamente", "id_user": user_id}


@router.put("/user/{user_id}/permissions")
async def update_user_permissions(
    user_id: int,
    body: UserPermissionsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and current_user.type_user_id != 1:
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")

    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if body.type_user_id not in (1, 2, 3, 4):
        raise HTTPException(status_code=400, detail="El tipo de usuario debe ser 1, 2, 3 o 4")

    # No permitir dejar el sistema sin administradores activos
    if not body.is_admin and user.type_user_id != 1 and user.is_admin:
        admins_activos = db.query(User).filter(
            User.is_admin == True,
            User.is_active == True
        ).count()
        if admins_activos <= 1:
            raise HTTPException(status_code=400, detail="No se puede quitar el permiso al último administrador activo")

    user.type_user_id = body.type_user_id
    user.is_admin = body.is_admin
    db.commit()
    return {"message": "Permisos actualizados exitosamente", "id_user": user_id}
