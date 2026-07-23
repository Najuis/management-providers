from app.database.get_db import get_db
from app.models.model_user import User
from app.middleware.hasher import hasher

db = next(get_db())

# Verificar si ya existe
user = db.query(User).filter(User.email == "admin@lagobo.com").first()
if user:
    print("⚠️ El usuario admin ya existe")
else:
    nuevo_user = User(
        email="admin@lagobo.com",
        password=hasher("Admin123!"),
        type_user_id=1,
        is_active=True,
        is_admin=True
    )
    db.add(nuevo_user)
    db.commit()
    print("✅ Admin creado exitosamente!")
    print("   Email: admin@lagobo.com")
    print("   Contraseña: Admin123!")

db.close()
