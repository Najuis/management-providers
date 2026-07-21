from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base
from datetime import datetime

# Importación condicional para evitar ciclos, pero SQLAlchemy resuelve el string "Submission" en runtime
if TYPE_CHECKING:
    from app.models.submission_models import Submission

class User(Base):
    __tablename__ = "lmp_user"
    
    id_user: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(150))
    type_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_type_user.id_type"))
    
    # ✅ Campos nuevos para compatibilidad
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # ============================================
    # RELACIONES EXISTENTES
    # ============================================
    user_type: Mapped["TypeUser"] = relationship(back_populates="user")
    general_information: Mapped["GeneralInformation"] = relationship(back_populates="user")
    natural_person: Mapped["NaturalPerson"] = relationship(back_populates="user")
    legal_person: Mapped["LegalPerson"] = relationship(back_populates="user")
    tax_fiscal_information: Mapped["TaxFiscalInformation"] = relationship(back_populates="user")
    financial_information: Mapped["FinancialInformation"] = relationship(back_populates="user")
    legal_representative_information: Mapped[List["LegalRepresentativeInformation"]] = relationship(back_populates="user")
    share_composition: Mapped[List["InfoShareComposition"]] = relationship(back_populates="user")
    references: Mapped[List["References"]] = relationship(back_populates="user")
    ohs_requirements: Mapped[List["OccupationalHealthSafetyRequirements"]] = relationship(back_populates="user")
    health_safety_requirements: Mapped[List["HealthSafetyRequirements"]] = relationship(back_populates="user")
    required_documents: Mapped[List["RequiredDocuments"]] = relationship(back_populates="user")
    authorizations_policies: Mapped["AuthorizationsPolicies"] = relationship(back_populates="user")
    
    # ============================================
    # ✅ RELACIÓN CON SUBMISSIONS (LA QUE FALTABA)
    # ============================================
    submissions: Mapped[List["Submission"]] = relationship(
        "Submission", 
        back_populates="user",
        foreign_keys="Submission.user_id"
    )

    # ============================================
    # PROPIEDADES DE COMPATIBILIDAD
    # ============================================
    @property
    def id(self) -> int:
        """Alias para compatibilidad con el router"""
        return self.id_user

    @property
    def role(self):
        """Retorna un objeto con la propiedad 'name' basado en type_user_id o is_admin"""
        class Role:
            name: str
        role = Role()
        if self.is_admin or self.type_user_id == 1:
            role.name = "admin"
        else:
            role.name = "user"
        return role

    def __repr__(self) -> str:
        return f"<User(id={self.id_user}, email={self.email})>"