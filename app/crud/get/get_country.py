from sqlalchemy.orm import Session
from app.models.model_country import Country
from fastapi import HTTPException

async def get_country_db(db: Session):
    try:
        countries = db.query(Country).all()
        if countries is None:
            raise HTTPException(status_code=404, detail="Country not found")
        return countries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
