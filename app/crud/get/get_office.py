from sqlalchemy.orm import Session
from app.models.model_office import Office
from fastapi import HTTPException

async def get_office_db(db: Session):
    try:
        offices = db.query(Office).all()
        if offices is None:
            raise HTTPException(status_code=404, detail="Office not found")
        return offices
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))