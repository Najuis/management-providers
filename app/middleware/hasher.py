from argon2 import PasswordHasher

def get_password_hash(password: str) -> str:
    """
    Hashea una contraseña usando Argon2.
    
    Args:
        password: Contraseña en texto plano
    
    Returns:
        str: Contraseña hasheada
    """
    ph = PasswordHasher()
    return ph.hash(password)

# Alias para compatibilidad con código existente
hasher = get_password_hash

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con un hash.
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Contraseña hasheada
    
    Returns:
        bool: True si coinciden, False si no
    """
    ph = PasswordHasher()
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except Exception:
        return False