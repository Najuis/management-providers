from pydantic import BaseModel

class InfoUser(BaseModel):
    email: str
    password: str
    type_user_id: int
    identification_type_id: int
    name: str
    phone: str
    document: str
    address: str
    region_id: int
    city_id: int
    country_id: int
    office_id: int