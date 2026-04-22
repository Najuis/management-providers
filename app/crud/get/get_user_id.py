from sqlalchemy.orm import Session
from app.models.model_user import User
from fastapi import HTTPException

async def get_user_id_db(db: Session, id_user):
    try:
        user = db.query(User).filter(User.id_user == id_user).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))