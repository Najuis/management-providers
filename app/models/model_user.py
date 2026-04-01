from __future__ import annotations
from typing import List
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

import datetime

class User(Base):
    __tablename__ = "lmp_user"

    id_user: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)    
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String(150))
    type_user: Mapped[int] = mapped_column(Integer, ForeignKey('lmp_type_user.id_type')) 
    create_at: Mapped[str] = mapped_column(DateTime, default=datetime.datetime.now)

    user_type: Mapped["TypeUser"] = relationship(back_populates="user")
    financial_information: Mapped[List["FinancialInformation"]] = relationship(back_populates="user")
    ohs_requirements: Mapped[List["OccupationalHealthSafetyRequirements"]] = relationship(back_populates="user")
    health_safety_requirements: Mapped[List["HealthSafetyRequirements"]] = relationship(back_populates="user")
    info_user: Mapped[List["InfoUser"]] = relationship(back_populates="user")
    references: Mapped[List["References"]] = relationship(back_populates="user")
    required_documents: Mapped[List["RequiredDocuments"]] = relationship(back_populates="user")
