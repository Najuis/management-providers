# app/crud/post/post_login.py
from fastapi import HTTPException, status
from app.models.model_user import User
from app.middleware.hasher import verify_password
from app.middleware.security import create_access_token
from datetime import timedelta

async def login(credentials, db):
    # 1. Buscar usuario por email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    # 2. Validar que exista y la contraseña sea correcta
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Validar que el usuario esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo. Contacte al administrador."
        )

    # 4. Crear el token de acceso
    access_token_expires = timedelta(minutes=60) # O el tiempo que uses
    access_token = create_access_token(
        data={"id_user": user.id_user, "type_user": user.type_user_id},
        expires_delta=access_token_expires
    )

    # ✅ 5. RETORNO CRÍTICO: Debe incluir 'type_user' para que el frontend funcione
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "type_user": user.type_user_id,  # <--- ESTO ES LO QUE EL FRONTEND NECESITA
        "is_admin": user.is_admin,
        "email": user.email
    }