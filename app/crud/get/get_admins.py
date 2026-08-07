from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.model_user import User

def get_all_admins_db(db: Session):
    try:
        admins = db.query(User).filter(
            or_(
                User.is_admin == True,
                User.type_user_id == 1
            )
        ).all()
        return admins
    except Exception as e:
        print(f"Error al obtener los administradores: {e}")
        return None
