from pydantic import BaseModel
from datetime import datetime

class TokenPayload(BaseModel):

    id_user: int
    type_user: int
    exp: datetime | None

class Token(BaseModel):
    access_token: str
    token_type: str

class DataTokenUser(BaseModel):
    type_user: int