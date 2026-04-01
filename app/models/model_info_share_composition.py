from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class InfoShareComposition(Base):
    __tablename__ = "lmp_info_share_composition"

    id_share_composition: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type_identification: Mapped[str] = mapped_column(String(50),nullable=True)
    number_identification: Mapped[str] = mapped_column(String(50),nullable=True)
    social_reason: Mapped[str] = mapped_column(String(150),nullable=True)
    name_complete: Mapped[str] = mapped_column(String(100),nullable=True)
    porcentage_porcentage: Mapped[float] = mapped_column(Float,nullable=True)
    