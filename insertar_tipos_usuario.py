"""
Script para insertar los tipos de usuario en la base de datos
Ejecutar: python insertar_tipos_usuario.py
"""
from app.database.get_db import get_db
from app.models.model_type_user import TypeUser

def insertar_tipos_usuario():
    db = next(get_db())
    
    try:
        # Verificar si ya existen
        existing = db.query(TypeUser).all()
        
        if not existing:
            print("📝 Creando tipos de usuario...\n")
            
            # Crear tipos de usuario
            admin_type = TypeUser(id_type=1, name="Administrador")
            user_type = TypeUser(id_type=2, name="Usuario Normal")
            
            db.add_all([admin_type, user_type])
            db.commit()
            
            print("✅ Tipos de usuario creados exitosamente:")
            print("   ID 1: Administrador")
            print("   ID 2: Usuario Normal")
        else:
            print("ℹ️  Los tipos de usuario ya existen:")
            for t in existing:
                print(f"   ID {t.id_type}: {t.name}")
                
        print("\n🎯 Ahora puedes crear usuarios desde el panel de administrador")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al insertar tipos de usuario: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    insertar_tipos_usuario()
