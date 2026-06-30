from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base  # ✅ Importar directamente desde base
from datetime import datetime
import enum

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

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Información general
    fecha = Column(DateTime, nullable=False)
    tipo_cliente = Column(String(50), nullable=False)
    tipo_vinculacion = Column(String(50), nullable=False)
    ciudad_id = Column(Integer, nullable=False)
    oficina = Column(String(100), nullable=False)
    tipo_persona = Column(String(20), nullable=False)
    
    # Identificación
    nombres = Column(String(200), nullable=True)
    apellidos = Column(String(200), nullable=True)
    razon_social = Column(String(300), nullable=True)
    tipo_id = Column(String(20), nullable=False)
    numero_id = Column(String(50), nullable=False, index=True)
    fecha_expedicion = Column(DateTime, nullable=True)
    estructura_juridica = Column(String(100), nullable=True)
    
    # Actividad económica
    codigo_ciiu = Column(String(20), nullable=False)
    pais_origen_id = Column(Integer, nullable=False)
    pais_residencia_id = Column(Integer, nullable=False)
    zona = Column(String(20), nullable=False)
    
    # Información financiera
    regimen_tributario = Column(String(50), nullable=False)
    total_ingresos = Column(Float, nullable=True)
    total_egresos = Column(Float, nullable=True)
    
    # ✅ NUEVO: Datos completos del formulario en JSON (para generar PDF)
    form_data = Column(Text, nullable=True)
    
    # ✅ Autorizaciones con Boolean (CORREGIDO)
    aut_datos = Column(Boolean, nullable=False, default=False)
    aut_laft = Column(Boolean, nullable=False, default=False)
    aut_anticorrupcion = Column(Boolean, nullable=False, default=False)
    aut_etica = Column(Boolean, nullable=False, default=False)
    
    # ✅ Estado y riesgo con String (CORREGIDO)
    status = Column(String(50), default=SubmissionStatus.BORRADOR.value)
    risk_level = Column(String(50), nullable=True)
    observations = Column(Text, nullable=True)
    validation_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    validated_at = Column(DateTime, nullable=True)
    
    # Relaciones
    documents = relationship("SubmissionDocument", back_populates="submission", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="submission", cascade="all, delete-orphan")

class SubmissionDocument(Base):
    __tablename__ = "submission_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    document_type = Column(String(100), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(200), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    submission = relationship("Submission", back_populates="documents")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(50), nullable=False)
    comments = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    submission = relationship("Submission", back_populates="audit_logs")