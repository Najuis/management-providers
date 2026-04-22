from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class TypeDocument(Base):
    __tablename__ = "lmp_type_document"

    id_type_document: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Relations
    user: Mapped[List["User"]] = relationship(back_populates="type_document")