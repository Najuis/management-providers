from __future__ import annotations
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base


class AuthorizationsPolicies(Base):
    __tablename__ = "lmp_authorizations_policies"

    id_authorization: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"))

    document_number: Mapped[str] = mapped_column(String(60))
    expedition_place: Mapped[str] = mapped_column(String(100))
    acting_as: Mapped[str] = mapped_column(String(100))  
    ciiu_code: Mapped[str] = mapped_column(String(20))
    economic_activity: Mapped[str] = mapped_column(String(200))
    
    licit_origin: Mapped[bool] = mapped_column(Boolean, default=False)
    knowledge_normativity: Mapped[bool] = mapped_column(Boolean, default=False)
    no_third_party_deposits: Mapped[bool] = mapped_column(Boolean, default=False)
    reality_statement: Mapped[bool] = mapped_column(Boolean, default=False)
    sagrilat_verification: Mapped[bool] = mapped_column(Boolean, default=False)

    # Preguntas PEP (Personas Expuestas Públicamente)
    public_resources: Mapped[bool] = mapped_column(Boolean, default=False)
    public_power: Mapped[bool] = mapped_column(Boolean, default=False)
    public_recognition: Mapped[bool] = mapped_column(Boolean, default=False)
    pep_link: Mapped[bool] = mapped_column(Boolean, default=False)
    pep_position: Mapped[str] = mapped_column(String(100), nullable=True)
    pep_link_date: Mapped[str] = mapped_column(String(60), nullable=True)
    
    # Autorización de consulta en listas restrictivas
    authorize_restrictive_lists: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Política de Transparencia y Ética Empresarial
    policy_adherence: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="authorizations_policies")
