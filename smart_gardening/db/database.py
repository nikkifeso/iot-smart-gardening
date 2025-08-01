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
    """Remove a plant from the database."""
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
    """Get a plant by its ID."""
    if plant_id is None or not isinstance(plant_id, int) or plant_id <= 0:
        return None
    return session.query(PlantModel).filter(PlantModel.id == plant_id).first()

def get_zone_by_id(zone_id: int) -> ZoneModel:
    """Get a zone by its ID."""
    if zone_id is None or not isinstance(zone_id, int) or zone_id <= 0:
        return None
    return session.query(ZoneModel).filter(ZoneModel.id == zone_id).first()

def cleanup_old_sensor_readings(retention_days: int = 60, db_session=None):
    """Remove sensor readings older than the specified number of days."""
    if db_session is None:
        db_session = session
        
    try:     
        cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=retention_days)
        
        deleted_count = db_session.query(SensorReading).filter(
            SensorReading.timestamp < cutoff_date
        ).delete()
        
        deleted_pump_logs = db_session.query(PumpLog).filter(
            PumpLog.timestamp < cutoff_date
        ).delete()
        
        db_session.commit()
        
        print(f"Data cleanup completed: {deleted_count} sensor readings and {deleted_pump_logs} pump logs older than {retention_days} days removed.")
        
        return deleted_count + deleted_pump_logs
        
    except Exception as e:
        db_session.rollback()
        print(f"Error during data cleanup: {e}")
        return 0

def get_sensor_readings_stats():
    """Get statistics about sensor readings in the database."""
    try:
        total_count = session.query(SensorReading).count()
        oldest_record = session.query(SensorReading).order_by(SensorReading.timestamp.asc()).first()
        newest_record = session.query(SensorReading).order_by(SensorReading.timestamp.desc()).first()
        
        stats = {
            'total_readings': total_count,
            'oldest_record': oldest_record.timestamp if oldest_record else None,
            'newest_record': newest_record.timestamp if newest_record else None,
        }
        
        if oldest_record and newest_record:
            stats['date_range_days'] = (newest_record.timestamp - oldest_record.timestamp).days
        
        return stats
        
    except Exception as e:
        print(f"Error getting sensor readings stats: {e}")
        return {}

def init_db():
    Base.metadata.create_all(engine)
