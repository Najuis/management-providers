import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.database.get_db import get_db
from app.crud.get.get_type_document import get_type_document_db

routes = fastapi.APIRouter()

@routes.get("/document_types")
async def get_document_types(
    db: Session = Depends(get_db)
):
    response = await get_type_document_db(db)

    if response:
        return {"message": response}
    else:
        return {"error": "Error al obtener los tipos de documento"}
        