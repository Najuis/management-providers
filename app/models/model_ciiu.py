from __future__ import annotations
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class CIIU(Base):
    __tablename__ = "lmp_ciiu"

    id_ciiu: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False)

    def __repr__(self):
        return f"<CIIU(codigo={self.codigo})>"
