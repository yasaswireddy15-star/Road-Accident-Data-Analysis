from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from database.connection import Base

class Location(Base):
    __tablename__ = "locations"
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(String(120), nullable=False, index=True)
    road_name = Column(String(160), nullable=True)
    accidents = relationship("Accident", back_populates="location")

class Accident(Base):
    __tablename__ = "accidents"
    accident_id = Column(Integer, primary_key=True, autoincrement=True)
    accident_datetime = Column(DateTime, nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("locations.location_id"), nullable=False)
    vehicle_type = Column(String(80), nullable=False, index=True)
    severity = Column(String(20), nullable=False, index=True)
    weather = Column(String(80), nullable=True)
    location = relationship("Location", back_populates="accidents")

Index("ix_accident_location_datetime", Accident.location_id, Accident.accident_datetime)
