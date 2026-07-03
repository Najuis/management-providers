"""
Script para agregar columnas faltantes a la tabla lmp_user
Ejecutar: python agregar_columnas.py
"""
from app.database.get_db import get_db
from sqlalchemy import text

def agregar_columnas():
    """Agregar columnas is_active, is_admin y created_at a lmp_user"""
    
    print("\n🔧 Agregando columnas faltantes a la tabla lmp_user...\n")
    
    db = next(get_db())
    
    try:
        # Verificar y agregar is_active
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'lmp_user' AND column_name = 'is_active'
        """))
        
        if not result.fetchone():
            print("✅ Agregando columna 'is_active'...")
            db.execute(text("ALTER TABLE lmp_user ADD COLUMN is_active BOOLEAN DEFAULT TRUE"))
        else:
            print("✓ Columna 'is_active' ya existe")
        
        # Verificar y agregar is_admin
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'lmp_user' AND column_name = 'is_admin'
        """))
        
        if not result.fetchone():
            print("✅ Agregando columna 'is_admin'...")
            db.execute(text("ALTER TABLE lmp_user ADD COLUMN is_admin BOOLEAN DEFAULT FALSE"))
        else:
            print("✓ Columna 'is_admin' ya existe")
        
        # Verificar y agregar created_at
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'lmp_user' AND column_name = 'created_at'
        """))
        
        if not result.fetchone():
            print("✅ Agregando columna 'created_at'...")
            db.execute(text("ALTER TABLE lmp_user ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
        else:
            print("✓ Columna 'created_at' ya existe")
        
        db.commit()
        
        print("\n✅ ¡Columnas agregadas exitosamente!")
        print("🎯 Ahora puedes ejecutar: python crear_admin.py\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error al agregar columnas: {e}\n")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    agregar_columnas()