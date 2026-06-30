from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
import json
from datetime import datetime

# ✅ IMPORTS CORREGIDOS (rutas reales del proyecto)
from app.database.get_db import get_db
from app.models.submission_models import Submission, SubmissionDocument, AuditLog, SubmissionStatus, RiskLevel
from app.models.user import User
from app.services.pdf_generator import generate_official_pdf
from app.services.risk_calculator import calculate_risk
from app.middleware.current_user import get_current_user

router = APIRouter()

UPLOAD_DIR = "app/uploads"

# --- 1. Descargar PDF Oficial ---
@router.get("/{submission_id}/download-pdf")
async def download_pdf(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    # Verificar permisos (solo dueño o admin)
    if submission.user_id != current_user.id and current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    # Generar PDF
    file_path = f"{UPLOAD_DIR}/{submission_id}/formulario_{submission_id}.pdf"
    
    # Si no existe, lo generamos
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # ✅ CORREGIDO: Usar form_data del modelo (debe agregarse al modelo)
        if hasattr(submission, 'form_data') and submission.form_data:
            data = json.loads(submission.form_data) if isinstance(submission.form_data, str) else submission.form_data
        else:
            # Fallback: construir data desde los campos del modelo
            data = {
                "fecha": submission.fecha.isoformat() if submission.fecha else "",
                "tipo_cliente": submission.tipo_cliente,
                "tipo_vinculacion": submission.tipo_vinculacion,
                "tipo_persona": submission.tipo_persona,
                "nombres": submission.nombres,
                "apellidos": submission.apellidos,
                "razon_social": submission.razon_social,
                "numero_id": submission.numero_id,
            }
        
        generate_official_pdf(data, file_path)

    return FileResponse(file_path, media_type='application/pdf', filename=f"formulario_{submission_id}.pdf")


# --- 2. Subir Documentos Firmados ---
@router.post("/{submission_id}/upload-docs")
async def upload_documents(
    submission_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    if submission.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Solo el propietario puede subir documentos")
    
    # ✅ CORREGIDO: Usar .value para comparar con String
    if submission.status != SubmissionStatus.BORRADOR.value:
        raise HTTPException(status_code=400, detail="La solicitud ya fue enviada o está en revisión")

    # Crear carpeta para esta submission
    user_upload_dir = f"{UPLOAD_DIR}/{submission_id}"
    os.makedirs(user_upload_dir, exist_ok=True)

    try:
        for file in files:
            file_path = f"{user_upload_dir}/{file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # ✅ CORREGIDO: Usar document_type (no file_type)
            doc_record = SubmissionDocument(
                submission_id=submission_id,
                document_type="anexo",
                file_path=file_path,
                file_name=file.filename,
                uploaded_by=current_user.id
            )
            db.add(doc_record)
        
        # ✅ CORREGIDO: Usar .value para asignar String
        submission.status = SubmissionStatus.PENDIENTE_REVISION.value
        submission.submitted_at = datetime.utcnow()
        db.commit()
        
        return {
            "message": "Documentos subidos exitosamente. Solicitud enviada a revisión.",
            "status": submission.status
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al subir archivos: {str(e)}")


# --- 3. Validar / Aprobar / Rechazar (Solo Admin) ---
@router.put("/{submission_id}/validate")
async def validate_submission(
    submission_id: int,
    action: str,  # 'APROBADO' o 'RECHAZADO'
    comments: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")

    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    # ✅ CORREGIDO: Usar .value para comparar con String
    if submission.status != SubmissionStatus.PENDIENTE_REVISION.value:
        raise HTTPException(status_code=400, detail="La solicitud no está pendiente de revisión")

    # ✅ CORREGIDO: Usar .value para asignar String
    if action.upper() == "APROBADO":
        new_status = SubmissionStatus.APROBADO.value
    elif action.upper() == "RECHAZADO":
        new_status = SubmissionStatus.RECHAZADO.value
    else:
        raise HTTPException(status_code=400, detail="Acción inválida. Use APROBADO o RECHAZADO")

    # Actualizar submission
    submission.status = new_status
    submission.updated_at = datetime.utcnow()
    
    # Registrar Auditoría
    audit_log = AuditLog(
        submission_id=submission_id,
        user_id=current_user.id,
        action=action.upper(),
        comments=comments,
        ip_address="127.0.0.1",
        user_agent="AdminPanel"
    )
    db.add(audit_log)
    db.commit()

    return {
        "message": f"Solicitud {action.lower()} correctamente",
        "new_status": new_status
    }