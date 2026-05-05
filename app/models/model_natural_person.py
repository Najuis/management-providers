from __future__ import annotations
from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base


class NaturalPerson(Base):
    __tablename__ = "lmp_natural_person"

    id_natural_person: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"))
    type_document_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_type_document.id_type_document"))
    municipality_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_municipality.id_municipality"))
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_region.id_region"))
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_country.id_country"))

    name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    document: Mapped[str] = mapped_column(String(60))
    expedition_date: Mapped[str] = mapped_column(String(60))
    birth_date: Mapped[str] = mapped_column(String(60))
    address: Mapped[str] = mapped_column(String(100))
    zone: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(60))
    company_name: Mapped[str] = mapped_column(String(100))
    nit: Mapped[str] = mapped_column(String(60))
    occupation: Mapped[str] = mapped_column(String(60))
    monthly_income: Mapped[float] = mapped_column(Float)
    other_income: Mapped[float] = mapped_column(Float)
    specify: Mapped[str] = mapped_column(String(100))

    # Relations
    user: Mapped["User"] = relationship(back_populates="natural_person")
    type_document: Mapped["TypeDocument"] = relationship(back_populates="natural_person")
    municipality: Mapped["Municipality"] = relationship(back_populates="natural_person")
    region: Mapped["Region"] = relationship(back_populates="natural_person")
    country: Mapped["Country"] = relationship(back_populates="natural_person")
