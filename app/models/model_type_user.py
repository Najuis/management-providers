
from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class TypeUser(Base):
    __tablename__ = 'lmp_type_user'

    id_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    
    user: Mapped[List["User"]] = relationship(back_populates="user_type")
