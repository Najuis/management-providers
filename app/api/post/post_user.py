from fastapi import Depends, APIRouter, Request
from app.schemas.info_user import InfoUser
from app.crud.post.post_user import post_user
from app.database.get_db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/info_user")
async def info_user(user: InfoUser, db: Session = Depends(get_db)):
    return await post_user(user, db)