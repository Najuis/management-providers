from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database.base import Base

class SubmissionStatus(str, enum.Enum):
    BORRADOR = "borrador"
    PENDIENTE_REVISION = "pendiente_revision"
    REVISADO = "revisado"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"

class RiskLevel(str, enum.Enum):
    BAJO = "bajo"
    MEDIO = "medio"
    ALTO = "alto"

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Datos del formulario (resumen o JSON completo si es muy grande)
    # Puedes expandir esto con columnas específicas si lo prefieres
    form_data = Column(Text, nullable=False)  # Guardaremos el JSON del formulario aquí
    
    # Cálculos automáticos
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.BAJO)
    ciiu_code = Column(String(50), nullable=True)
    country_origin = Column(String(100), nullable=True)
    
    # Estados y Fechas
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.BORRADOR)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True) # Fecha cuando se envía a revisión

    # Relaciones
    documents = relationship("SubmissionDocument", back_populates="submission", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="submission", cascade="all, delete-orphan")
    user = relationship("User", back_populates="submissions")

class SubmissionDocument(Base):
    __tablename__ = "submission_documents"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    
    file_type = Column(String(50), nullable=False) # 'pdf_firmado', 'anexo_rut', etc.
    file_path = Column(String(255), nullable=False) # Ruta relativa en el servidor
    file_name = Column(String(255), nullable=False) # Nombre original del archivo
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    submission = relationship("Submission", back_populates="documents")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Quién hizo la acción
    
    action = Column(String(50), nullable=False) # 'APROBADO', 'RECHAZADO', 'COMENTARIO'
    comments = Column(Text, nullable=True) # Observaciones del auditor
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    submission = relationship("Submission", back_populates="audit_logs")