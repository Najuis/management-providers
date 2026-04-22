from app.models.model_user import User
from app.middleware.check_password import check_password
from app.middleware.create_token import create_token

async def login(user, db):
    
    data_user = db.query(User).filter(User.email == user.email).first()

    if not data_user:

        return {"status":404, "detail":"User no found"}
    
    if not check_password(user.password, data_user.password):

        return {"status":401, "detail":"Incorrect password"}


    response = await create_token(data_user)

    return response