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
    type_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('lmp_type_user.id_type')) 
    identification_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_type_document.id_type_document"),nullable=True)
    name: Mapped[str] = mapped_column(String(150),nullable=True)
    phone: Mapped[str] = mapped_column(String(20),nullable=True)
    document: Mapped[str] = mapped_column(String(20),nullable=True)  
    address: Mapped[str] = mapped_column(String(255),nullable=True)
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_region.id_region"),nullable=True)       
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_city.id_city"),nullable=True)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_country.id_country"),nullable=True)    
    office_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_office.id_office"),nullable=True)
    create_at: Mapped[str] = mapped_column(DateTime, default=datetime.datetime.now)

    user_type: Mapped["TypeUser"] = relationship(back_populates="user")
    ohs_requirements: Mapped["OccupationalHealthSafetyRequirements"] = relationship(back_populates="user")
    health_safety_requirements: Mapped["HealthSafetyRequirements"] = relationship(back_populates="user")
    financial_information: Mapped["FinancialInformation"] = relationship(back_populates="user")
    references: Mapped["References"] = relationship(back_populates="user")
    required_documents: Mapped["RequiredDocuments"] = relationship(back_populates="user")
    type_document: Mapped["TypeDocument"] = relationship(back_populates="user")
    region: Mapped["Region"] = relationship(back_populates="user")
    city: Mapped["City"] = relationship(back_populates="user")
    country: Mapped["Country"] = relationship(back_populates="user")
    office: Mapped["Office"] = relationship(back_populates="user")
