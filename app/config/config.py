from fastapi import HTTPException, status
from datetime import timedelta
from typing import Final
from dotenv import load_dotenv
import os

load_dotenv()

# ============================================

# ============================================
#
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
   
    pg_user = os.getenv('PG_USER')
    pg_password = os.getenv('PG_DB_PASSWORD')
    pg_host = os.getenv('PG_HOST', 'localhost')
    pg_port = os.getenv('PG_PORT', '5432')
    pg_database = os.getenv('PG_DATABASE')
    
    if pg_user and pg_password and pg_database:
        DATABASE_URL = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
    else:
     
        DATABASE_URL = "sqlite:///./management_providers.db"

# ============================================

# ============================================
SECRET_KEY = os.environ.get("SECRET_KEY", "cambiar-en-produccion-minimo-32-caracteres-2024")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = 40
ACCESS_TOKEN_EXPIRES: Final[timedelta] = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)