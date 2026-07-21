"""
Script para crear las tablas en la base de datos
Ejecutar: python crear_tablas.py
"""
from app.database.core import create_tables

if __name__ == "__main__":
    print("🔧 Creando tablas en la base de datos...")
    create_tables()
    print("✅ ¡Tablas creadas exitosamente!")
    print("\n📋 Tablas creadas:")
    print("   - lmp_user")
    print("   - submissions")
    print("   - submission_documents")
    print("   - audit_logs")
    print("   - ... y todas las demás tablas")
