# db/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///smart_garden.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class ZoneModel(Base):
    __tablename__ = 'zones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    plant_type = Column(String)
    moisture_threshold = Column(Integer, default=30)
    ph_min = Column(Float, default=6.0)
    ph_max = Column(Float, default=7.5)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_watered = Column(DateTime, nullable=True)

class PlantModel(Base):
    __tablename__ = 'plants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    zone_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    plant_type = Column(String, nullable=False)
    planting_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class SensorReading(Base):
    __tablename__ = 'sensor_readings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    zone_id = Column(Integer, nullable=False)
    moisture = Column(Float)
    ph = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class PumpLog(Base):
    __tablename__ = 'pump_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    zone_id = Column(Integer, nullable=False)
    status = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Create tables
def init_db():
    Base.metadata.create_all(engine)
