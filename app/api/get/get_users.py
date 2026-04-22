import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.middleware.current_user import current_user
from app.database.get_db import get_db
from app.crud.get.get_users import get_all_users_db

routes = fastapi.APIRouter()

@routes.get("/users")
async def get_all_users(
    db: Session = Depends(get_db),
    user: dict = Depends(current_user)
):
    if user["type_user"] != 1:
        return HTTPException(status_code=401, detail="Unauthorized")
    else:
        response = get_all_users_db(db)
        
        if response:
            return {"message": response}
        else:
            return {"error": "Error al obtener los usuarios"}
        
        