from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base


class Office(Base):
    __tablename__ = "lmp_office"

    id_office: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String)
    office_name: Mapped[str] = mapped_column(String)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_city.id_city"))

    # Relations
    city: Mapped["City"] = relationship(back_populates="office")
    general_information: Mapped[List["GeneralInformation"]] = relationship(back_populates="office")
