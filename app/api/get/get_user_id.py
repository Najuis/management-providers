import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.database.get_db import get_db
from app.crud.get.get_user_id import get_user_id_db
from app.middleware.current_user import current_user

routes = fastapi.APIRouter()

@routes.get("/userbyid")
async def get_user_id(
    id_user: int,
    db: Session = Depends(get_db),
    user: dict = Depends(current_user)
):
    print(user)
    if user["type_user"] != 1:
        raise HTTPException(status_code=401, detail="Unauthorized")

    response = await get_user_id_db(db, id_user)
    return {"message": response}

        