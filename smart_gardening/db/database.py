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
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

def remove_plant(plant_id: int, db_session=None) -> bool:
    """
    Remove a plant from the database.
    
    Args:
        plant_id: The ID of the plant to remove
        db_session: Database session to use (defaults to global session)
        
    Returns:
        bool: True if plant was successfully removed, False otherwise
    """
    if plant_id is None or not isinstance(plant_id, int) or plant_id <= 0:
        return False
        
    if db_session is None:
        db_session = session
        
    try:
        plant = db_session.query(PlantModel).filter(PlantModel.id == plant_id).first()
        if plant:
            db_session.delete(plant)
            db_session.commit()
            return True
        return False
    except Exception as e:
        db_session.rollback()
        print(f"Error removing plant: {e}")
        return False

def get_plant_by_id(plant_id: int) -> PlantModel:
    """
    Get a plant by its ID.
    
    Args:
        plant_id: The ID of the plant to retrieve
        
    Returns:
        PlantModel: The plant object or None if not found
    """
    if plant_id is None or not isinstance(plant_id, int) or plant_id <= 0:
        return None
    return session.query(PlantModel).filter(PlantModel.id == plant_id).first()

def get_zone_by_id(zone_id: int) -> ZoneModel:
    """
    Get a zone by its ID.
    
    Args:
        zone_id: The ID of the zone to retrieve
        
    Returns:
        ZoneModel: The zone object or None if not found
    """
    if zone_id is None or not isinstance(zone_id, int) or zone_id <= 0:
        return None
    return session.query(ZoneModel).filter(ZoneModel.id == zone_id).first()

def init_db():
    Base.metadata.create_all(engine)
