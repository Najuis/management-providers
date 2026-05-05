from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base


class Municipality(Base):
    __tablename__ = "lmp_municipality"

    id_municipality: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    municipality_name: Mapped[str] = mapped_column(String(100))
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_region.id_region"))

    # Relations
    region: Mapped["Region"] = relationship(back_populates="municipality")
    natural_person: Mapped[List["NaturalPerson"]] = relationship(back_populates="municipality")
    legal_person: Mapped[List["LegalPerson"]] = relationship(back_populates="municipality")
