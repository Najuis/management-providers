from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class LegalPerson(Base):
    __tablename__ = "lmp_legal_person"

    id_legal_person: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    reason_or_name: Mapped[str] = mapped_column(String(100))
    nit: Mapped[str] = mapped_column(String(60))
    address: Mapped[str] = mapped_column(String(100))
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_region.id_region"))
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_city.id_city"))
    society_type: Mapped[str] = mapped_column(String(60))
    link_type: Mapped[str] = mapped_column(String(60))
    municipality_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_municipality.id_municipality"), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"))

    region: Mapped["Region"] = relationship(back_populates="legal_person")
    city: Mapped["City"] = relationship(back_populates="legal_person")
    user: Mapped["User"] = relationship(back_populates="legal_person")
    municipality: Mapped["Municipality"] = relationship(back_populates="legal_person")

    legal_representative_information: Mapped[List["LegalRepresentativeInformation"]] = relationship(back_populates="legal_person")
    info_share_composition: Mapped[List["InfoShareComposition"]] = relationship(back_populates="legal_person")