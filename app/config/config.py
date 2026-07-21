from fastapi import HTTPException, status
from datetime import timedelta
from typing import Final
from dotenv import load_dotenv
import os

load_dotenv() 

# DATABASE_URL = f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_DB_PASSWORD')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DATABASE')}"
DATABASE_URL = "sqlite:///./management_providers.db"

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = 40
ACCESS_TOKEN_EXPIRES: Final[timedelta] = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)