import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.database.get_db import get_db
from app.crud.get.get_city import get_city_db

routes = fastapi.APIRouter()

@routes.get("/city")
async def get_city(
    db: Session = Depends(get_db)
):
    response = await get_city_db(db)

    if response:
        return {"message": response}
    else:
        return {"error": "Error al obtener las ciudades"}