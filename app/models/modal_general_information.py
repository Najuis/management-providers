from __future__ import annotations
from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class GeneralInformation(Base):
    __tablename__ = "lmp_general_information"

    id_general_information: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"))
    date_information: Mapped[str] = mapped_column(String)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_city.id_city"))
    office_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_office.id_office"))
    
    user: Mapped["User"] = relationship(back_populates="general_information")
    city: Mapped["City"] = relationship(back_populates="general_information")
    office: Mapped["Office"] = relationship(back_populates="general_information")