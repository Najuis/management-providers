from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, BackgroundTasks, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import os
import shutil
import json

# ✅ IMPORTS CORREGIDOS (rutas reales del proyecto)
from app.database.get_db import get_db
from app.models.submission_models import Submission, SubmissionDocument, AuditLog, SubmissionStatus, RiskLevel
from app.models.model_user import User
from app.services.pdf_generator import generate_official_pdf
from app.services.risk_calculator import calculate_risk
from app.middleware.current_user import get_current_user

router = APIRouter()

# ✅ CORREGIDO: Era PLOAD_DIR (faltaba la "U")
UPLOAD_DIR = "app/uploads"


# ============================================
# SCHEMA PARA CREAR SUBMISSION
# ============================================
class SubmissionCreate(BaseModel):
    fecha: str
    tipo_cliente: str
    tipo_vinculacion: str
    ciudad_id: int
    oficina: str
    tipo_persona: str
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    razon_social: Optional[str] = None
    tipo_id: str
    numero_id: str
    fecha_expedicion: Optional[str] = None
    estructura_juridica: Optional[str] = None
    codigo_ciiu: str
    pais_origen_id: int
    pais_residencia_id: int
    zona: str
    regimen_tributario: str
    total_ingresos: Optional[float] = None
    total_egresos: Optional[float] = None
    aut_datos: bool = False
    aut_laft: bool = False
    aut_anticorrupcion: bool = False
    aut_etica: bool = False


# ============================================
# ENDPOINTS GET (DEBEN IR ANTES QUE POST CON MISMA RUTA)
# ============================================

# --- 0. LISTAR SOLICITUDES (GET /api/submissions) ---
@router.get("")
async def list_submissions(
    status_filter: Optional[str] = Query(None, alias="status"),  # ✅ Renombrado para evitar conflicto
    risk: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar todas las solicitudes con filtros"""
    query = db.query(Submission)
    
    if status_filter and status_filter != 'all':
        query = query.filter(Submission.status == status_filter)
    
    if risk:
        query = query.filter(Submission.risk_level == risk)
    
    submissions = query.order_by(Submission.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "submissions": submissions,
        "total": len(submissions),
        "skip": skip,
        "limit": limit
    }


# --- 0.1. OBTENER DETALLES DE UNA SOLICITUD (GET /api/submissions/{id}) ---
@router.get("/{submission_id}")
async def get_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener detalles completos de una solicitud"""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    documents = db.query(SubmissionDocument).filter(
        SubmissionDocument.submission_id == submission_id
    ).all()
    
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
        ]
    }


# ============================================
# ENDPOINT POST: CREAR NUEVA SOLICITUD
# ============================================
@router.post("")
async def create_submission(
    submission_data: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crear una nueva solicitud de vinculación de terceros.
    """
    try:
        # 1. Calcular nivel de riesgo
        risk_level = calculate_risk(
            pais_origen_id=submission_data.pais_origen_id,
            ciudad_id=submission_data.ciudad_id,
            codigo_ciiu=submission_data.codigo_ciiu
        )
        
        # 2. Parsear fecha (si viene como string ISO)
        fecha_obj = datetime.fromisoformat(submission_data.fecha) if submission_data.fecha else datetime.utcnow()
        
        # 3. Crear nueva submission
        new_submission = Submission(
            user_id=current_user.id_user,
            fecha=fecha_obj,
            tipo_cliente=submission_data.tipo_cliente,
            tipo_vinculacion=submission_data.tipo_vinculacion,
            ciudad_id=submission_data.ciudad_id,
            oficina=submission_data.oficina,
            tipo_persona=submission_data.tipo_persona,
            nombres=submission_data.nombres,
            apellidos=submission_data.apellidos,
            razon_social=submission_data.razon_social,
            tipo_id=submission_data.tipo_id,
            numero_id=submission_data.numero_id,
            fecha_expedicion=datetime.fromisoformat(submission_data.fecha_expedicion) if submission_data.fecha_expedicion else None,
            estructura_juridica=submission_data.estructura_juridica,
            codigo_ciiu=submission_data.codigo_ciiu,
            pais_origen_id=submission_data.pais_origen_id,
            pais_residencia_id=submission_data.pais_residencia_id,
            zona=submission_data.zona,
            regimen_tributario=submission_data.regimen_tributario,
            total_ingresos=submission_data.total_ingresos,
            total_egresos=submission_data.total_egresos,
            aut_datos=submission_data.aut_datos,
            aut_laft=submission_data.aut_laft,
            aut_anticorrupcion=submission_data.aut_anticorrupcion,
            aut_etica=submission_data.aut_etica,
            status=SubmissionStatus.PENDIENTE_REVISION.value,
            risk_level=risk_level,
            submitted_at=datetime.utcnow()
        )
        
        # 4. Guardar en BD
        db.add(new_submission)
        db.commit()
        db.refresh(new_submission)
        
        # 5. Crear directorio para documentos
        user_upload_dir = f"{UPLOAD_DIR}/{new_submission.id}"
        os.makedirs(user_upload_dir, exist_ok=True)
        
        # 6. Generar PDF automáticamente
        pdf_data = {
            "fecha": new_submission.fecha.isoformat() if new_submission.fecha else "",
            "tipo_cliente": new_submission.tipo_cliente,
            "tipo_vinculacion": new_submission.tipo_vinculacion,
            "tipo_persona": new_submission.tipo_persona,
            "nombres": new_submission.nombres,
            "apellidos": new_submission.apellidos,
            "razon_social": new_submission.razon_social,
            "tipo_id": new_submission.tipo_id,
            "numero_id": new_submission.numero_id,
            "codigo_ciiu": new_submission.codigo_ciiu,
            "pais_origen_id": new_submission.pais_origen_id,
            "pais_residencia_id": new_submission.pais_residencia_id,
            "zona": new_submission.zona,
            "regimen_tributario": new_submission.regimen_tributario,
            "total_ingresos": new_submission.total_ingresos,
            "total_egresos": new_submission.total_egresos,
            "aut_datos": new_submission.aut_datos,
            "aut_laft": new_submission.aut_laft,
            "aut_anticorrupcion": new_submission.aut_anticorrupcion,
            "aut_etica": new_submission.aut_etica,
            "risk_level": risk_level,
        }
        
        pdf_path = f"{user_upload_dir}/formulario_{new_submission.id}.pdf"
        try:
            generate_official_pdf(pdf_data, pdf_path)
        except Exception as pdf_error:
            print(f"⚠️  Error generando PDF: {pdf_error}")
        
        return {
            "message": "Solicitud creada exitosamente",
            "submission_id": new_submission.id,
            "risk_level": risk_level,
            "status": new_submission.status
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error al crear solicitud: {str(e)}"
        )


# ============================================
# ENDPOINTS EXISTENTES (MANTENIDOS)
# ============================================

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
    # ✅ CORREGIDO: Usar id_user consistentemente
    if submission.user_id != current_user.id_user and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="No autorizado")

    # Generar PDF
    file_path = f"{UPLOAD_DIR}/{submission_id}/formulario_{submission_id}.pdf"
    
    # Si no existe, lo generamos
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Usar form_data del modelo si existe
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
    
    # ✅ CORREGIDO: Usar id_user consistentemente
    if submission.user_id != current_user.id_user:
        raise HTTPException(status_code=403, detail="Solo el propietario puede subir documentos")
    
    # Usar .value para comparar con String
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
            
            # ✅ CORREGIDO: Usar document_type (no file_type) y id_user
            doc_record = SubmissionDocument(
                submission_id=submission_id,
                document_type="anexo",
                file_path=file_path,
                file_name=file.filename,
                uploaded_by=current_user.id_user
            )
            db.add(doc_record)
        
        # Usar .value para asignar String
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
    # ✅ CORREGIDO: Usar is_admin directamente
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")

    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    # Usar .value para comparar con String
    if submission.status != SubmissionStatus.PENDIENTE_REVISION.value:
        raise HTTPException(status_code=400, detail="La solicitud no está pendiente de revisión")

    # Usar .value para asignar String
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
    # ✅ CORREGIDO: Usar id_user
    audit_log = AuditLog(
        submission_id=submission_id,
        user_id=current_user.id_user,
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