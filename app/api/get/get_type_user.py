import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.database.get_db import get_db
from app.crud.get.get_type_user import get_type_user_db

routes = fastapi.APIRouter()

@routes.get("/type_user")
async def get_type_user(
    db: Session = Depends(get_db)
):
    response = await get_type_user_db(db)

    if response:
        return {"message": response}
    else:
        return {"error": "Error al obtener los tipos de usuario"}
        