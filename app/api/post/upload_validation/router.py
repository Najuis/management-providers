from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import shutil
import json

from app.database.get_db import get_db
from app.models.submission_models import Submission, SubmissionDocument, AuditLog, SubmissionStatus
from app.models.model_user import User
from app.services.pdf_generator import generate_official_pdf
from app.middleware.current_user import get_current_user
from app.schemas.submission import SubmissionCreate

router = APIRouter()
UPLOAD_DIR = "app/uploads"

# ============================================
# HELPERS
# ============================================
def get_client_ip(request: Request) -> str:
    """Obtiene la IP real del cliente, manejando proxies o ngrok."""
    return request.client.host if request.client else "unknown"


def serialize_submission(submission: Submission, documents: Optional[list] = None) -> dict:
    """Convierte una Submission de SQLAlchemy en un dict JSON serializable."""
    return {
        "id": submission.id,
        "user_id": submission.user_id,
        "fecha": submission.fecha.isoformat() if submission.fecha else None,
        "tipo_cliente": submission.tipo_cliente,
        "tipo_vinculacion": submission.tipo_vinculacion,
        "ciudad_id": submission.ciudad_id,
        "oficina": submission.oficina,
        "tipo_persona": submission.tipo_persona,
        "nombres": submission.nombres,
        "apellidos": submission.apellidos,
        "razon_social": submission.razon_social,
        "nombre": submission.nombres if submission.tipo_persona != "juridica" else submission.razon_social,
        "tipo_cliente_display": "Persona Jurídica" if submission.tipo_persona == "juridica" else "Persona Natural",
        "tipo_id": submission.tipo_id,
        "numero_id": submission.numero_id,
        "fecha_expedicion": submission.fecha_expedicion.isoformat() if submission.fecha_expedicion else None,
        "estructura_juridica": submission.estructura_juridica,
        "codigo_ciiu": submission.codigo_ciiu,
        "pais_origen_id": submission.pais_origen_id,
        "pais_residencia_id": submission.pais_residencia_id,
        "zona": submission.zona,
        "regimen_tributario": submission.regimen_tributario,
        "total_ingresos": submission.total_ingresos,
        "total_egresos": submission.total_egresos,
        "aut_datos": submission.aut_datos,
        "aut_laft": submission.aut_laft,
        "aut_anticorrupcion": submission.aut_anticorrupcion,
        "aut_etica": submission.aut_etica,
        "status": submission.status,
        "risk_level": submission.risk_level,
        "observations": submission.observations,
        "validation_notes": submission.validation_notes,
        "created_at": submission.created_at.isoformat() if submission.created_at else None,
        "updated_at": submission.updated_at.isoformat() if submission.updated_at else None,
        "submitted_at": submission.submitted_at.isoformat() if submission.submitted_at else None,
        "validated_at": submission.validated_at.isoformat() if submission.validated_at else None,
        "documents": (documents or []),
        "form_data": json.loads(submission.form_data) if submission.form_data else {}
    }


# ============================================
# ENDPOINTS
# ============================================

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_submission(
    payload: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crea una solicitud de vinculación con estado 'pendiente_revision'."""
    raw = payload.model_dump(exclude_unset=True)

    submission = Submission(
        user_id=current_user.id_user,
        fecha=payload.fecha or datetime.utcnow(),
        tipo_cliente=payload.tipo_cliente,
        tipo_vinculacion=payload.tipo_vinculacion,
        ciudad_id=payload.ciudad_id,
        oficina=payload.oficina,
        tipo_persona=payload.tipo_persona,
        nombres=payload.nombres,
        apellidos=payload.apellidos,
        razon_social=payload.razon_social,
        tipo_id=payload.tipo_id,
        numero_id=payload.numero_id,
        fecha_expedicion=payload.fecha_expedicion,
        estructura_juridica=payload.estructura_juridica,
        codigo_ciiu=payload.codigo_ciiu,
        pais_origen_id=payload.pais_origen_id,
        pais_residencia_id=payload.pais_residencia_id,
        zona=payload.zona,
        regimen_tributario=payload.regimen_tributario,
        total_ingresos=payload.total_ingresos,
        total_egresos=payload.total_egresos,
        aut_datos=payload.aut_datos,
        aut_laft=payload.aut_laft,
        aut_anticorrupcion=payload.aut_anticorrupcion,
        aut_etica=payload.aut_etica,
        form_data=json.dumps(raw, ensure_ascii=False, default=str),
        status=SubmissionStatus.PENDIENTE_REVISION.value,
        submitted_at=datetime.utcnow(),
    )

    try:
        db.add(submission)
        db.commit()
        db.refresh(submission)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la solicitud: {str(e)}")

    return {
        "id": submission.id,
        "status": submission.status,
        "message": "Solicitud creada correctamente"
    }


@router.get("", response_model=dict)
async def list_submissions(
    status_filter: Optional[str] = None,
    risk: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Submission)
    if status_filter and status_filter != 'all':
        query = query.filter(Submission.status == status_filter)
    if risk:
        query = query.filter(Submission.risk_level == risk)
    
    submissions = query.order_by(Submission.created_at.desc()).offset(skip).limit(limit).all()
    total = query.count()

    serialized = [serialize_submission(s) for s in submissions]

    return {"submissions": serialized, "total": total, "skip": skip, "limit": limit}


@router.get("/{submission_id}")
async def get_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    documents = db.query(SubmissionDocument).filter(
        SubmissionDocument.submission_id == submission_id
    ).all()
    
    # ✅ Mapeo manual (vuelve al enfoque original que funcionaba)
    return {
        "id": submission.id,
        "user_id": submission.user_id,
        "fecha": submission.fecha.isoformat() if submission.fecha else None,
        "tipo_cliente": submission.tipo_cliente,
        "tipo_vinculacion": submission.tipo_vinculacion,
        "ciudad_id": submission.ciudad_id,
        "oficina": submission.oficina,
        "tipo_persona": submission.tipo_persona,
        "nombres": submission.nombres,
        "apellidos": submission.apellidos,
        "razon_social": submission.razon_social,
        "tipo_id": submission.tipo_id,
        "numero_id": submission.numero_id,
        "fecha_expedicion": submission.fecha_expedicion.isoformat() if submission.fecha_expedicion else None,
        "estructura_juridica": submission.estructura_juridica,
        "codigo_ciiu": submission.codigo_ciiu,
        "pais_origen_id": submission.pais_origen_id,
        "pais_residencia_id": submission.pais_residencia_id,
        "zona": submission.zona,
        "regimen_tributario": submission.regimen_tributario,
        "total_ingresos": submission.total_ingresos,
        "total_egresos": submission.total_egresos,
        "aut_datos": submission.aut_datos,
        "aut_laft": submission.aut_laft,
        "aut_anticorrupcion": submission.aut_anticorrupcion,
        "aut_etica": submission.aut_etica,
        "status": submission.status,
        "risk_level": submission.risk_level,
        "observations": submission.observations,
        "validation_notes": submission.validation_notes,
        "created_at": submission.created_at.isoformat() if submission.created_at else None,
        "updated_at": submission.updated_at.isoformat() if submission.updated_at else None,
        "submitted_at": submission.submitted_at.isoformat() if submission.submitted_at else None,
        "validated_at": submission.validated_at.isoformat() if submission.validated_at else None,
        "documents": [
            {
                "id": doc.id,
                "document_type": doc.document_type,
                "file_path": doc.file_path,
                "file_name": doc.file_name,
                "uploaded_at": doc.uploaded_at.isoformat() if doc.uploaded_at else None
            }
            for doc in documents
        ],
        "form_data": json.loads(submission.form_data) if submission.form_data else {}
    }


@router.get("/{submission_id}/download-pdf")
async def download_pdf(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    if submission.user_id != current_user.id_user and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    file_path = f"{UPLOAD_DIR}/{submission_id}/formulario_{submission_id}.pdf"
    
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if hasattr(submission, 'form_data') and submission.form_data:
            data = json.loads(submission.form_data) if isinstance(submission.form_data, str) else submission.form_data
        else:
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


@router.post("/{submission_id}/upload-docs", status_code=status.HTTP_201_CREATED)
async def upload_documents(
    submission_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    if submission.user_id != current_user.id_user:
        raise HTTPException(status_code=403, detail="Solo el propietario puede subir documentos")
    
    if submission.status != SubmissionStatus.BORRADOR.value:
        raise HTTPException(status_code=400, detail="La solicitud ya fue enviada o está en revisión")
    
    user_upload_dir = f"{UPLOAD_DIR}/{submission_id}"
    os.makedirs(user_upload_dir, exist_ok=True)
    
    ALLOWED_EXTENSIONS = {".pdf"}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    try:
        for file in files:
            # 1. Validación de Seguridad: Extensión
            _, ext = os.path.splitext(file.filename)
            if ext.lower() not in ALLOWED_EXTENSIONS:
                raise HTTPException(status_code=400, detail=f"Tipo de archivo no permitido: {ext}")
            
            # 2. Validación de Seguridad: Tamaño
            file.file.seek(0, os.SEEK_END)
            if file.file.tell() > MAX_FILE_SIZE:
                raise HTTPException(status_code=413, detail="El archivo excede el límite de 5MB")
            file.file.seek(0)

            file_path = f"{user_upload_dir}/{file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            doc_record = SubmissionDocument(
                submission_id=submission_id,
                document_type="anexo",
                file_path=file_path,
                file_name=file.filename,
                uploaded_by=current_user.id_user
            )
            db.add(doc_record)
        
        submission.status = SubmissionStatus.PENDIENTE_REVISION.value
        submission.submitted_at = datetime.utcnow()
        db.commit()
        
        return {
            "message": "Documentos subidos exitosamente. Solicitud enviada a revisión.", 
            "status": submission.status
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno al procesar archivos: {str(e)}")


@router.post("/{submission_id}/upload-form", status_code=status.HTTP_201_CREATED)
async def upload_signed_form(
    submission_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    if submission.user_id != current_user.id_user and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="No autorizado")

    ALLOWED_EXTENSIONS = {".pdf"}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Tipo de archivo no permitido: {ext}")

    file.file.seek(0, os.SEEK_END)
    if file.file.tell() > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="El archivo excede el límite de 5MB")
    file.file.seek(0)

    user_upload_dir = f"{UPLOAD_DIR}/{submission_id}"
    os.makedirs(user_upload_dir, exist_ok=True)
    safe_name = f"formulario_firmado{ext.lower()}"
    file_path = f"{user_upload_dir}/{safe_name}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    existing = db.query(SubmissionDocument).filter(
        SubmissionDocument.submission_id == submission_id,
        SubmissionDocument.document_type == "formulario_firmado"
    ).first()
    if existing:
        existing.file_path = file_path
        existing.file_name = safe_name
        existing.uploaded_at = datetime.utcnow()
    else:
        db.add(SubmissionDocument(
            submission_id=submission_id,
            document_type="formulario_firmado",
            file_path=file_path,
            file_name=safe_name,
            uploaded_by=current_user.id_user
        ))
    db.commit()

    return {
        "message": "Formulario de vinculación firmado cargado exitosamente",
        "file_name": safe_name
    }


@router.put("/{submission_id}/validate")
async def validate_submission(
    submission_id: int,
    action: str,
    request: Request,               # ✅ CORREGIDO: Movido ANTES de los parámetros con default
    comments: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")
    
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    if submission.status != SubmissionStatus.PENDIENTE_REVISION.value:
        raise HTTPException(status_code=400, detail="La solicitud no está pendiente de revisión")
    
    action_upper = action.upper()
    if action_upper == "APROBADO":
        new_status = SubmissionStatus.APROBADO.value
    elif action_upper == "RECHAZADO":
        new_status = SubmissionStatus.RECHAZADO.value
    else:
        raise HTTPException(status_code=400, detail="Acción inválida. Use APROBADO o RECHAZADO")
    
    submission.status = new_status
    submission.updated_at = datetime.utcnow()
    
    audit_log = AuditLog(
        submission_id=submission_id,
        user_id=current_user.id_user,
        action=action_upper,
        comments=comments,
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("user-agent", "Unknown")
    )
    db.add(audit_log)
    db.commit()
    
    return {
        "message": f"Solicitud {action.lower()} correctamente", 
        "new_status": new_status
    }