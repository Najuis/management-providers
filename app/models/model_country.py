from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class Country(Base):
    __tablename__ = "lmp_country"

    id_country: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    
    # Relations
    user: Mapped[List["User"]] = relationship(back_populates="country")