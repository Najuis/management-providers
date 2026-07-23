from __future__ import annotations
from typing import List, Optional
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.core import Base

class Office(Base):
    __tablename__ = "lmp_office"

    id_office: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Campos de datos
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    zona: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    ciudad: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    departamento: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    direccion: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    director: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    corporativo: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    fijo: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    correo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # ✅ Foreign Key para la relación con City (¡ESTO FALTABA!)
    city_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("lmp_city.id_city"), nullable=True)

    # Relaciones
    city: Mapped["City"] = relationship(back_populates="office")
    general_information: Mapped[List["GeneralInformation"]] = relationship(back_populates="office")

    def __repr__(self):
        return f"<Office(nombre={self.nombre}, ciudad={self.ciudad})>"