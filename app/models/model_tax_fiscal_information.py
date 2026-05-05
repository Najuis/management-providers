from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class TaxFiscalInformation(Base):
    __tablename__ = "lmp_tax_fiscal_information"

    id_tax_fiscal: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    common: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    big_taxpayer: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    simplified_regime: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    self_retained_resolution: Mapped[str] = mapped_column(String(60), nullable=True)
    self_retained_date: Mapped[str] = mapped_column(String(60), nullable=True)

    big_taxpayer_resolution: Mapped[str] = mapped_column(String(60), nullable=True)
    big_taxpayer_date: Mapped[str] = mapped_column(String(60), nullable=True)

    self_retained_ica_resolution: Mapped[str] = mapped_column(String(60), nullable=True)
    self_retained_ica_date: Mapped[str] = mapped_column(String(60), nullable=True)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"))

    
    user: Mapped["User"] = relationship(back_populates="tax_fiscal_information")

    
    
