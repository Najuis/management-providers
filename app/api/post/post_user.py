from fastapi import Depends, APIRouter, Request, HTTPException
from app.schemas.info_user import InfoUser
from app.crud.post.post_user import post_user
from app.database.get_db import get_db
from sqlalchemy.orm import Session
from app.middleware.current_user import current_user

router = APIRouter()

@router.post("/info_user")
async def info_user(
    user_info: InfoUser,
    db: Session = Depends(get_db),
    user: dict = Depends(current_user)
):
    if user["type_user"] != 2:
        return HTTPException(status_code=401, detail="Unauthorized")
    return await post_user(user_info, db)