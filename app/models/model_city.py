from __future__ import annotations
from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class City(Base):
    __tablename__ = "lmp_city"

    id_city: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    region_id: Mapped[int] = mapped_column(ForeignKey('lmp_region.id_region'), nullable=True)

    #Relations
    office: Mapped[List["Office"]] = relationship(back_populates="city")
    user: Mapped[List["User"]] = relationship(back_populates="city")
    region: Mapped["Region"] = relationship(back_populates="city")
    legal_representative_information: Mapped[List["LegalRepresentativeInformation"]] = relationship(back_populates="city")
