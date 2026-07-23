from app.database.get_db import get_db
from app.models.model_user import User
from app.middleware.hasher import hasher

def crear_usuario():
    print("🔧 Conectando a la base de datos...")
    db = next(get_db())
    
    try:
        email = "prueba1@lagobo.com"
        password = "123456"
        
        # Verificar si ya existe
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"⚠️ El usuario {email} ya existe en la base de datos.")
            return
            
        print(f"📝 Creando usuario: {email}...")
        nuevo_user = User(
            email=email,
            password=hasher(password),
            type_user_id=1,  # Administrador
            is_active=True,
            is_admin=True
        )
        
        db.add(nuevo_user)
        db.commit()
        print("✅ Usuario creado exitosamente!")
        print(f"   Email: {email}")
        print(f"   Contraseña: {password}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al crear el usuario: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    crear_usuario()
