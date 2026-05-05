from pydantic import BaseModel

class InfoUser(BaseModel):
    email: str
    password: str
    type_user_id: int