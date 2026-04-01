from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class LegalEntities(Base):
    __tablename__ = "lmp_legal_entities"

    id_legal_entities: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name_society_social: Mapped[str] = mapped_column(String(150),nullable=True)
    number_nit: Mapped[str] = mapped_column(String(100),nullable=True)   
    society_type: Mapped[str] = mapped_column(String(100),nullable=True)  
    type_bonding: Mapped[str] = mapped_column(String(100),nullable=True)
