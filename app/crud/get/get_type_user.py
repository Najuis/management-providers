from sqlalchemy.orm import Session
from app.models.model_type_user import TypeUser
from fastapi import HTTPException

async def get_type_user_db(db: Session):
    try:
        type_user = db.query(TypeUser).all()
        return [t.to_dict() for t in type_user]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
