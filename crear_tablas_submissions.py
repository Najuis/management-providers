"""
Script para crear tablas de Submissions faltantes
Ejecutar: python crear_tablas_submissions.py
"""
from app.database.core import engine
from app.models.submission_models import Submission, SubmissionDocument, AuditLog

def crear_tablas_submissions():
    print("🔧 Creando tablas de Submissions...\n")
    
    try:
        # Crear cada tabla individualmente
        Submission.__table__.create(engine, checkfirst=True)
        print("✅ Tabla 'submissions' creada")
        
        SubmissionDocument.__table__.create(engine, checkfirst=True)
        print("✅ Tabla 'submission_documents' creada")
        
        AuditLog.__table__.create(engine, checkfirst=True)
        print("✅ Tabla 'audit_logs' creada")
        
        print("\n🎯 Todas las tablas de Submissions están listas")
        
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    crear_tablas_submissions()
