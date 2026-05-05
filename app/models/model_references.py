from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class References(Base):
    __tablename__ = "lmp_references"

    id_reference: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"))   

    bank_name: Mapped[str] = mapped_column(String(150), nullable=True)
    titular_name: Mapped[str] = mapped_column(String(150), nullable=True)
    account_type: Mapped[str] = mapped_column(String(50), nullable=True)
    social_reason: Mapped[str] = mapped_column(String(150), nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    number_telephone: Mapped[str] = mapped_column(String(50), nullable=True)
    
    #Relations
    user: Mapped["User"] = relationship(back_populates="references")