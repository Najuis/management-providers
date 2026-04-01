from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class OccupationalHealthSafetyRequirements(Base):
    __tablename__ = "lmp_occupational_health_safety_requirements"

    id_ohs_requirement: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"))
    
    # Occupational Health & Safety fields
    document: Mapped[str] = mapped_column(String(150), nullable=True)
    fulfilled: Mapped[bool] = mapped_column(Boolean, default=False)
    observation: Mapped[str] = mapped_column(String(255), nullable=True)    
    
    # Relations
    user: Mapped["User"] = relationship(back_populates="ohs_requirements")