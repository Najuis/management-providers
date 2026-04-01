from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class RequiredDocuments(Base):
    __tablename__ = "lmp_required_documents"

    id_document: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_user.id_user"))
    
    # Required document tracking fields
    document_name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relations
    user: Mapped["User"] = relationship(back_populates="required_documents")
