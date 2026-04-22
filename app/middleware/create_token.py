from app.config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRES
from app.schemas.token import Token
from fastapi import HTTPException
from datetime import datetime
import jwt

async def create_token(data_user):

    if not SECRET_KEY or not ALGORITHM:
        raise HTTPException(
            status_code=500, 
            detail="Server misconfiguration: SECRET_KEY or ALGORITHM missing."
        )

    expire = datetime.utcnow() + ACCESS_TOKEN_EXPIRES

    to_encode = {
        "id_user": data_user.id_user,
        "type_user": data_user.type_user_id,
        "exp": expire
    }

    try:
        encoded_jwt = jwt.encode(
            to_encode,
            key=SECRET_KEY,
            algorithm=ALGORITHM
        )
        return Token(access_token=encoded_jwt, token_type="bearer")
    except Exception as e:
        print(f"Token generation error: {e}")
        raise HTTPException(status_code=500, detail="Error generating token")