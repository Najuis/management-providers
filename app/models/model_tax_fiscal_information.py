from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class TaxFiscalInformation(Base):
    __tablename__ = "lmp_tax_fiscal_information"

    id_tax_fiscal: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    common: Mapped[bool] = mapped_column(Boolean, nullable=True)
    big_taxpayer: Mapped[bool] = mapped_column(Boolean, nullable=True)
    simplified_regime: Mapped[bool] = mapped_column(Boolean, nullable=True)
    resolution_number: Mapped[str] = mapped_column(String(100), nullable=True)   
    date_resolution: Mapped[str] = mapped_column(String(50), nullable=True)