"""
Script para crear usuario administrador de pruebas
Ejecutar: python crear_admin.py
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def crear_usuario_admin():
    """Crear usuario admin en la base de datos"""
    
    # Importaciones dentro de la función para evitar errores de carga
    from app.database.get_db import get_db
    from app.models.model_user import User
    
    # Intentar importar la función de hash
    try:
        from app.middleware.hasher import hasher
        def hash_password(password: str) -> str:
            return hasher(password)
        print("✅ Función hasher importada desde app.middleware.hasher")
    except ImportError:
        try:
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            def hash_password(password: str) -> str:
                return pwd_context.hash(password)
            print("✅ Función hash_password creada con passlib (alternativa)")
        except ImportError:
            print("❌ No se pudo importar ninguna función de hash")
            print("   Instala passlib: pip install passlib[bcrypt]")
            sys.exit(1)
    
    # Credenciales
    email = "admin@lagobo.com"
    password = "Admin123!"
    
    print(f"\n🔐 Creando usuario administrador...")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"   Admin: True\n")
    
    # Obtener sesión de BD
    db = next(get_db())
    
    try:
        # Verificar si ya existe
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"⚠️  El usuario {email} ya existe con ID: {existing.id_user}")
            print("   No se creará un duplicado.")
            return
        
        # Crear usuario con los campos CORRECTOS del modelo
        nuevo_user = User(
            email=email,
            password=hash_password(password),  # ✅ Campo es 'password'
            type_user_id=1,                     # ✅ Admin
            is_active=True,
            is_admin=True
        )
        
        db.add(nuevo_user)
        db.commit()
        db.refresh(nuevo_user)
        
        print(f"✅ Usuario creado exitosamente!")
        print(f"   ID: {nuevo_user.id_user}")
        print(f"   Email: {nuevo_user.email}")
        print(f"   Admin: {nuevo_user.is_admin}")
        print(f"   Active: {nuevo_user.is_active}")
        print(f"\n🎯 Ahora puedes hacer login en:")
        print(f"   http://127.0.1.1:8000/login")
        print(f"\n📝 Credenciales:")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al crear usuario: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    crear_usuario_admin()