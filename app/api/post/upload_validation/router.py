from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime

from app.core.database import get_db
from app.models.submission_models import Submission, SubmissionDocument, AuditLog, SubmissionStatus, RiskLevel
from app.models.user import User
from app.services.pdf_generator import generate_official_pdf
from app.services.risk_calculator import calculate_risk
from app.core.security import get_current_user # Asumiendo que tienes este middleware

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

    # Generar PDF (esto podría optimizarse cacheando el archivo)
    file_path = f"{UPLOAD_DIR}/{submission_id}/formulario_{submission_id}.pdf"
    
    # Si no existe, lo generamos
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Asumimos que form_data es un JSON string, habría que parsearlo si es necesario
        import json
        data = json.loads(submission.form_data) if isinstance(submission.form_data, str) else submission.form_data
        generate_official_pdf(data, file_path)

    from fastapi.responses import FileResponse
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
    
    if submission.status != SubmissionStatus.BORRADOR:
        raise HTTPException(status_code=400, detail="La solicitud ya fue enviada o está en revisión")

    # Crear carpeta para esta submission
    user_upload_dir = f"{UPLOAD_DIR}/{submission_id}"
    os.makedirs(user_upload_dir, exist_ok=True)

    try:
        for file in files:
            file_path = f"{user_upload_dir}/{file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Registrar en BD
            doc_record = SubmissionDocument(
                submission_id=submission_id,
                file_type="anexo", # Podrías inferirlo del nombre o agregar un campo extra
                file_path=file_path,
                file_name=file.filename,
                uploaded_by=current_user.id
            )
            db.add(doc_record)
        
        # Cambiar estado a Pendiente Revisión
        submission.status = SubmissionStatus.PENDIENTE_REVISION
        submission.submitted_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Documentos subidos exitosamente. Solicitud enviada a revisión.", "status": submission.status}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al subir archivos: {str(e)}")


# --- 3. Validar / Aprobar / Rechazar (Solo Admin) ---
@router.put("/{submission_id}/validate")
async def validate_submission(
    submission_id: int,
    action: str, # 'APROBADO' o 'RECHAZADO'
    comments: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")

    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    if submission.status != SubmissionStatus.PENDIENTE_REVISION:
        raise HTTPException(status_code=400, detail="La solicitud no está pendiente de revisión")

    # Determinar nuevo estado
    if action.upper() == "APROBADO":
        new_status = SubmissionStatus.APROBADO
    elif action.upper() == "RECHAZADO":
        new_status = SubmissionStatus.RECHAZADO
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
        ip_address="127.0.0.1", # En producción usar request.client.host
        user_agent="AdminPanel" # En producción usar request.headers.get('user-agent')
    )
    db.add(audit_log)
    db.commit()

    return {"message": f"Solicitud {action.lower()} correctamente", "new_status": new_status}