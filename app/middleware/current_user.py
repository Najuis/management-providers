from app.config.config import SECRET_KEY, ALGORITHM, CREDENTIALS_EXCEPTION
from app.middleware.security import oauth2_scheme
from fastapi import Depends, HTTPException
from typing import Annotated
from app.schemas.token import TokenPayload
import jwt

async def current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenPayload:
    
    try:
        payload = jwt.decode(
            token, 
            key=SECRET_KEY, 
            algorithms=ALGORITHM
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    id_user = payload.get("id_user")
    type_user = payload.get("type_user")

    if id_user is None or type_user is None:
        raise CREDENTIALS_EXCEPTION
    return payload