import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.database.get_db import get_db
from app.crud.get.get_country import get_country_db

routes = fastapi.APIRouter()

@routes.get("/country")
async def get_country(
    db: Session = Depends(get_db)
):
    response = await get_country_db(db)

    if response:
        return {"message": response}
    else:
        return {"error": "Error al obtener las oficinas"}
        