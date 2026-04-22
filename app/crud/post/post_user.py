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
            identification_type_id=user.identification_type_id,
            name=user.name,
            phone=user.phone,
            document=user.document,
            address=user.address,
            region_id=user.region_id,
            city_id=user.city_id,
            country_id=user.country_id,
            office_id=user.office_id
        )
        db.execute(stmt)
        db.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        db.rollback()
        return {"message": str(e)}