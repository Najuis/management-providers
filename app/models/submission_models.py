from sqlalchemy import String, Integer, ForeignKey, Text, Boolean, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base
from datetime import datetime
import enum

# ============================================
# ENUMS
# ============================================
class SubmissionStatus(str, enum.Enum):
    BORRADOR = "borrador"
    PENDIENTE_REVISION = "pendiente_revision"
    EN_REVISION = "en_revision"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"
    COMPLETADO = "completado"

class RiskLevel(str, enum.Enum):
    BAJO = "bajo"
    MEDIO = "medio"
    ALTO = "alto"
    EXTREMO = "extremo"


# ============================================
# MODELO PRINCIPAL: SUBMISSION
# ============================================
class Submission(Base):
    __tablename__ = "submissions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"), nullable=True)
    
    # Información general
    fecha: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    tipo_cliente: Mapped[str] = mapped_column(String(50), nullable=False)
    tipo_vinculacion: Mapped[str] = mapped_column(String(50), nullable=False)
    ciudad_id: Mapped[int] = mapped_column(Integer, nullable=False)
    oficina: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo_persona: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Identificación
    nombres: Mapped[str] = mapped_column(String(200), nullable=True)
    apellidos: Mapped[str] = mapped_column(String(200), nullable=True)
    razon_social: Mapped[str] = mapped_column(String(300), nullable=True)
    tipo_id: Mapped[str] = mapped_column(String(20), nullable=False)
    numero_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    fecha_expedicion: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    estructura_juridica: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Actividad económica
    codigo_ciiu: Mapped[str] = mapped_column(String(20), nullable=False)
    pais_origen_id: Mapped[int] = mapped_column(Integer, nullable=True)
    pais_residencia_id: Mapped[int] = mapped_column(Integer, nullable=True)
    zona: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # Información financiera
    regimen_tributario: Mapped[str] = mapped_column(String(50), nullable=False)
    total_ingresos: Mapped[float] = mapped_column(Float, nullable=True)
    total_egresos: Mapped[float] = mapped_column(Float, nullable=True)
    
    # Datos completos del formulario en JSON
    form_data: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Autorizaciones
    aut_datos: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    aut_laft: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    aut_anticorrupcion: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    aut_etica: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    # Estado y riesgo
    status: Mapped[str] = mapped_column(String(50), default=SubmissionStatus.BORRADOR.value)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=True)
    observations: Mapped[str] = mapped_column(Text, nullable=True)
    validation_notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    validated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Relaciones
    user: Mapped["User"] = relationship("User", back_populates="submissions")
    documents: Mapped[list["SubmissionDocument"]] = relationship("SubmissionDocument", back_populates="submission", cascade="all, delete-orphan")
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="submission", cascade="all, delete-orphan")


# ============================================
# MODELO: DOCUMENTOS ADJUNTOS
# ============================================
class SubmissionDocument(Base):
    __tablename__ = "submission_documents"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    submission_id: Mapped[int] = mapped_column(Integer, ForeignKey("submissions.id"), nullable=False)
    document_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_name: Mapped[str] = mapped_column(String(200), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    uploaded_by: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"), nullable=True)
    
    submission: Mapped["Submission"] = relationship("Submission", back_populates="documents")


# ============================================
# MODELO: LOG DE AUDITORÍA
# ============================================
class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    submission_id: Mapped[int] = mapped_column(Integer, ForeignKey("submissions.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"), nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    comments: Mapped[str] = mapped_column(Text, nullable=True)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[str] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    submission: Mapped["Submission"] = relationship("Submission", back_populates="audit_logs")