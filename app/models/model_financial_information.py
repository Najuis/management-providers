from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class FinancialInformation(Base):
    __tablename__ = "lmp_financial_information"

    id_financial: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"))
    
    # Financial fields
    total_active: Mapped[float] = mapped_column(Float, nullable=True)
    total_passive: Mapped[float] = mapped_column(Float, nullable=True)
    total_equity: Mapped[float] = mapped_column(Float, nullable=True)   
    heritage: Mapped[float] = mapped_column(Float, nullable=True)
    monthly_expenditure: Mapped[float] = mapped_column(Float, nullable=True)
    monthly_income: Mapped[float] = mapped_column(Float, nullable=True)

    # Relations
    user: Mapped["User"] = relationship(back_populates="financial_information")