from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class LegalRepresentativeInformation(Base):
    __tablename__ = "lmp_legal_representative_information"

    id_legal_representative_information: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_legal_representative: Mapped[str] = mapped_column(String(150),nullable=True)
    number_document: Mapped[str] = mapped_column(String(20),nullable=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_city.id_city"),nullable=True)
    phone: Mapped[str] = mapped_column(String(20),nullable=True)
    email: Mapped[str] = mapped_column(String(150),nullable=True)

    # Relations
    city: Mapped["City"] = relationship(back_populates="legal_representative_information")
