from __future__ import annotations
from typing import List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base


class Region(Base):
    __tablename__ = "lmp_region"

    id_region: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    # Relations
    city: Mapped[List["City"]] = relationship(back_populates="region")
    municipality: Mapped[List["Municipality"]] = relationship(back_populates="region")
    natural_person: Mapped[List["NaturalPerson"]] = relationship(back_populates="region")
    legal_person: Mapped[List["LegalPerson"]] = relationship(back_populates="region")
