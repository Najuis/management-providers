from app.config.config import CREDENTIALS_EXCEPTION
from app.middleware.security import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.database.get_db import get_db
from app.models.model_user import User
from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from jose import JWTError, jwt  # ✅ Usar python-jose (NO PyJWT)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
) -> User:
    """
    Obtener el usuario actual desde el token JWT.
    """
    try:
        # ✅ Decodificar token usando python-jose (misma librería que security.py)
        payload = jwt.decode(
            token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Extraer datos del payload
    id_user = payload.get("id_user")
    type_user = payload.get("type_user")
    
    # Validar que existan los campos requeridos
    if id_user is None or type_user is None:
        raise CREDENTIALS_EXCEPTION
    
    # Consultar usuario en la base de datos
    user = db.query(User).filter(User.id_user == id_user).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar que el usuario esté activo
    if hasattr(user, 'is_active') and not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return user

# Alias para compatibilidad con routers antiguos
current_user = get_current_user