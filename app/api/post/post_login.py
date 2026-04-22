from fastapi import Depends, APIRouter, Request
from app.schemas.login import Login
from app.crud.post.post_login import login as login_request
from app.database.get_db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/login")
async def login(credentials:Login, db: Session = Depends(get_db)):

    response = await login_request(credentials, db)
    
    return response