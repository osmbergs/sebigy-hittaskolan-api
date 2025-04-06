from datetime import datetime
from enum import StrEnum, auto

from narwhals import Int32
from sqlalchemy import Column, String, JSON, DateTime, Boolean, Integer, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.models.base import Base



class SchoolStatus(StrEnum):

    active = auto() #AKTIV
    paused = auto() #VILANDE
    cancelled=auto() #UPPHORT
    planned = auto() #PLANERAD


class SchoolType(StrEnum):

    Preliminary = auto() #FKLASS
    Elementary = auto() #GR
    ElementaryOther = auto()  # GRAN
    Recreational=auto() #FTH
    RecreationalOpen=auto() #OPPFTH
    Special=auto() #SP
    Minority=auto() #SAM
    Secondary = auto()  # GR
    SecondaryOther = auto()  # GRAN
    Adult = auto()  # VUX


class School(Base):
    __tablename__ = "school"
    id: Column[str] | str = Column(String, primary_key=True, index=True)
    status: Column[str] | str = Column(String, nullable=False)

    types:  Column[JSONB]  = Column(JSONB,index=True)

    school_unit_code: Column[str] | str = Column(String, nullable=False,index=True)
    created: Column[datetime] | datetime = Column(DateTime)
    updated: Column[datetime] | datetime = Column(DateTime)
    name: Column[str] | str = Column(String, nullable=False)
    display_name: Column[str] | str = Column(String, nullable=True)
    url: Column[str] | str = Column(String, nullable=True)
    email: Column[str] | str = Column(String, nullable=True)
    phone: Column[str] | str = Column(String, nullable=True)
    headmaster: Column[str] | str = Column(String, nullable=True)
    municipality_code: Column[str] | str = Column(String, nullable=True)

    visit_address_street: Column[str] | str = Column(String, nullable=True)
    visit_address_postal_code: Column[str] | str = Column(String, nullable=True)
    visit_address_locality: Column[str] | str = Column(String, nullable=True)
    geo_lat: Column[str] | str = Column(String, nullable=True)
    geo_long: Column[str] | str = Column(String, nullable=True)
    full_data: Column[bool] | str = Column(Boolean,default=False)

    image_url: Column[str] | str = Column(String, nullable=True)
    description: Column[str] | str = Column(String, nullable=True)


