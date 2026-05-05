from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class LegalRepresentativeInformation(Base):
    __tablename__ = "lmp_legal_representative_information"

    id_legal_representative_information: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"))
    name: Mapped[str] = mapped_column(String(60), nullable=True)
    last_name: Mapped[str] = mapped_column(String(60), nullable=True)
    document: Mapped[str] = mapped_column(String(60), nullable=True)
    phone: Mapped[str] = mapped_column(String(60), nullable=True)
    email: Mapped[str] = mapped_column(String(60), nullable=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_city.id_city"),nullable=True)
    legal_person_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_legal_person.id_legal_person"), nullable=True)

    user: Mapped["User"] = relationship(back_populates="legal_representative_information")
    city: Mapped["City"] = relationship(back_populates="legal_representative_information")
    legal_person: Mapped["LegalPerson"] = relationship(back_populates="legal_representative_information")