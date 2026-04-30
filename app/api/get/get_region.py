from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.get_db import get_db
from app.crud.get.get_region import get_region_db   

routes = APIRouter()

@routes.get("/regions")
async def get_regions(
    db: Session = Depends(get_db)
):
    response = await get_region_db(db)

    if response:
        return {"message": response}
    else:
        return {"error": "Error al obtener las regiones"}