from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.get_db import get_db
from app.crud.get.get_office import get_office_db

router = APIRouter()

@router.get("/office")
async def get_office(db: Session = Depends(get_db)):
    response = await get_office_db(db)
    if response:
        return {"message": response}
    else:
        return {"error": "Error al obtener las oficinas"}