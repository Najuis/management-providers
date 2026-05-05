from __future__ import annotations
from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base


class InfoShareComposition(Base):
    __tablename__ = "lmp_info_share_composition"

    id_share_composition: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"))
    legal_person_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_legal_person.id_legal_person"))

    identification_type: Mapped[str] = mapped_column(String(60), nullable=True)
    numero_identification: Mapped[str] = mapped_column(String(60), nullable=True)
    social_reason: Mapped[str] = mapped_column(String(60), nullable=True)
    full_name: Mapped[str] = mapped_column(String(60), nullable=True)
    percentage: Mapped[float] = mapped_column(Float, nullable=True)

    # Relations
    user: Mapped["User"] = relationship(back_populates="share_composition")
    legal_person: Mapped["LegalPerson"] = relationship(back_populates="info_share_composition")
