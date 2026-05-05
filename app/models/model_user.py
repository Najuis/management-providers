from __future__ import annotations
from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base


class User(Base):
    __tablename__ = "lmp_user"

    id_user: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String(150))
    type_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("lmp_type_user.id_type"))

    # Relations
    user_type: Mapped["TypeUser"] = relationship(back_populates="user")
    general_information: Mapped["GeneralInformation"] = relationship(back_populates="user")
    natural_person: Mapped["NaturalPerson"] = relationship(back_populates="user")
    legal_person: Mapped["LegalPerson"] = relationship(back_populates="user")
    tax_fiscal_information: Mapped["TaxFiscalInformation"] = relationship(back_populates="user")
    financial_information: Mapped["FinancialInformation"] = relationship(back_populates="user")
    legal_representative_information: Mapped[List["LegalRepresentativeInformation"]] = relationship(back_populates="user")
    share_composition: Mapped[List["InfoShareComposition"]] = relationship(back_populates="user")
    references: Mapped[List["References"]] = relationship(back_populates="user")
    ohs_requirements: Mapped[List["OccupationalHealthSafetyRequirements"]] = relationship(back_populates="user")
    health_safety_requirements: Mapped[List["HealthSafetyRequirements"]] = relationship(back_populates="user")
    required_documents: Mapped[List["RequiredDocuments"]] = relationship(back_populates="user")
    authorizations_policies: Mapped["AuthorizationsPolicies"] = relationship(back_populates="user")
