from sqlalchemy.orm import Session
from app.models.model_city import City

async def get_city_db(db: Session):
    try:
        cities = db.query(City).all()
        return cities
    except Exception as e:
        print(f"Error al obtener las ciudades: {e}")
        return None