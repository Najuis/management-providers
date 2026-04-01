from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class InfoUser(Base):
    __tablename__ = "lmp_info_user"

    id_info_user: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"),nullable=True)
    identification_type: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_type_document.id_type_document"),nullable=True)
    name: Mapped[str] = mapped_column(String(150),nullable=True)
    email: Mapped[str] = mapped_column(String(150),nullable=True)   
    phone: Mapped[str] = mapped_column(String(20),nullable=True)
    document: Mapped[str] = mapped_column(String(20),nullable=True)  
    address: Mapped[str] = mapped_column(String(255),nullable=True)
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_region.id_region"),nullable=True)       
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_city.id_city"),nullable=True)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_country.id_country"),nullable=True)    
    office_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_office.id_office"),nullable=True)

    #Relations
    user: Mapped["User"] = relationship(back_populates="info_user")
    city: Mapped["City"] = relationship(back_populates="info_user")
    office: Mapped["Office"] = relationship(back_populates="info_user")
    type_document: Mapped["TypeDocument"] = relationship(back_populates="info_user")
    region: Mapped["Region"] = relationship(back_populates="info_user")
    country: Mapped["Country"] = relationship(back_populates="info_user")

