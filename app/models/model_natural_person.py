from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class NaturalPerson(Base):
    __tablename__ = "lmp_natural_person"

    id_natural_person: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date_expedition: Mapped[str] = mapped_column(String(50),nullable=True)
    date_birth: Mapped[str] = mapped_column(String(50),nullable=True)
    zone: Mapped[str] = mapped_column(String(50), nullable=True)
    employee: Mapped[str] = mapped_column(String(50),nullable=True)
    number_nit: Mapped[str] = mapped_column(String(20),nullable=True)   
    charge: Mapped[str] = mapped_column(String(50),nullable=True)
    monthly_income: Mapped[float] = mapped_column(Float, nullable=True) 
    other_income: Mapped[float] = mapped_column(Float, nullable=True)