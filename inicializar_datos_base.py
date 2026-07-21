"""
Script para inicializar datos base del sistema
Ejecutar: python inicializar_datos_base.py
"""
from app.database.get_db import get_db
from app.models.model_type_user import TypeUser

def inicializar_datos_base():
    print("\n🔧 Inicializando datos base del sistema...\n")
    db = next(get_db())
    
    try:
        tipos_existentes = db.query(TypeUser).all()
        
        if not tipos_existentes:
            print("📝 Creando tipos de usuario...\n")
            tipos = [
                TypeUser(id_type=1, name="Administrador"),
                TypeUser(id_type=2, name="Usuario Normal"),
                TypeUser(id_type=3, name="Proveedor"),
                TypeUser(id_type=4, name="Cliente"),
            ]
            db.add_all(tipos)
            db.commit()
            print("✅ Tipos de usuario creados exitosamente:")
            for t in tipos:
                print(f"   ID {t.id_type}: {t.name}")
        else:
            print("ℹ️  Los tipos de usuario ya existen.")
            
        print("\n🎯 ¡Base de datos lista para usar!")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error al inicializar: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    inicializar_datos_base()