from sqlalchemy.orm import Session
from app.models.model_region import Region
from fastapi import HTTPException

async def get_region_db(db: Session):
    try:
        region = db.query(Region).all()
        return [r.to_dict() for r in region]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))