from app.middleware.hasher import hasher
from app.models.model_user import User
from sqlalchemy import insert

async def post_user(user, db):

    try:
        
        ph = hasher(user.password)
        
        stmt = insert(User).values(
            email=user.email,
            password=ph,
            type_user_id=user.type_user_id,
        )
        db.execute(stmt)
        db.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        db.rollback()
        return {"message": str(e)}