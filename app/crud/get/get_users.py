from sqlalchemy.orm import Session
from app.models.model_user import User

def get_all_users_db(db: Session):

    try:
        users = db.query(User).filter(User.type_user_id != 1).all()
        return users
    except Exception as e:
        print(f"Error al obtener los usuarios: {e}")
        return None

