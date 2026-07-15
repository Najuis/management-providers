from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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

@router.post("")
async def create_submission(
    submission_data: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear nueva solicitud de vinculación"""
    try:
        risk_level = calculate_risk(
            pais_origen_id=submission_data.pais_origen_id,
            ciudad_id=submission_data.ciudad_id,
            codigo_ciiu=submission_data.codigo_ciiu
        )
        
        fecha_obj = datetime.fromisoformat(submission_data.fecha) if submission_data.fecha else datetime.utcnow()
        
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
        
        db.add(new_submission)
        db.commit()
        db.refresh(new_submission)
        
        user_upload_dir = f"{UPLOAD_DIR}/{new_submission.id}"
        os.makedirs(user_upload_dir, exist_ok=True)
        
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
        raise HTTPException(status_code=500, detail=f"Error al crear solicitud: {str(e)}")