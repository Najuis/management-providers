from app.config.config import SECRET_KEY, ALGORITHM, CREDENTIALS_EXCEPTION
from app.middleware.security import oauth2_scheme
from app.database.get_db import get_db
from app.models.model_user import User
from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
import jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
) -> User:
    """
    Obtener el usuario actual desde el token JWT.
    
    Args:
        token: Token JWT del header Authorization
        db: Sesión de base de datos
    
    Returns:
        User: Objeto User completo de la base de datos
    
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    try:
        # Decodificar token
        payload = jwt.decode(
            token,
            key=SECRET_KEY,
            algorithms=ALGORITHM
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar token: {str(e)}"
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


# Alias para compatibilidad con el router
current_user = get_current_user
