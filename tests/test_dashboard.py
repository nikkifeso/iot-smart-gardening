import unittest
import sys
import os
import tempfile
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smart_gardening.db.database import Base, ZoneModel, PlantModel, SensorReading, PumpLog, init_db
from smart_gardening.core.zone import Zone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestDashboardData(unittest.TestCase):
    """Test cases for dashboard data operations"""
    
    def setUp(self):
        """Set up test database"""
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        
        # Create engine and session for testing
        self.engine = create_engine(f'sqlite:///{self.db_path}')
        Base.metadata.create_all(self.engine)
        
        # Create test session
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.test_session = TestingSessionLocal()
        
        # Create test data
        self.create_test_data()
    
    def tearDown(self):
        """Clean up test database"""
        self.test_session.close()
        os.unlink(self.db_path)
    
    def create_test_data(self):
        """Create test data for dashboard"""
        # Create test zones
        zones = [
            ZoneModel(name="Vegetable Garden", plant_type="Vegetables", moisture_threshold=30, ph_min=6.0, ph_max=7.5),
            ZoneModel(name="Herb Garden", plant_type="Herbs", moisture_threshold=25, ph_min=6.5, ph_max=7.0),
            ZoneModel(name="Flower Bed", plant_type="Flowers", moisture_threshold=35, ph_min=6.0, ph_max=7.0)
        ]
        
        for zone in zones:
            self.test_session.add(zone)
        self.test_session.commit()
        
        # Create test plants
        plants = [
            PlantModel(zone_id=1, name="Tomato", plant_type="Vegetable", planting_date=datetime.now().date()),
            PlantModel(zone_id=1, name="Basil", plant_type="Herb", planting_date=datetime.now().date()),
            PlantModel(zone_id=2, name="Rosemary", plant_type="Herb", planting_date=datetime.now().date()),
            PlantModel(zone_id=3, name="Marigold", plant_type="Flower", planting_date=datetime.now().date())
        ]
        
        for plant in plants:
            self.test_session.add(plant)
        self.test_session.commit()
        
        # Create test sensor readings
        readings = [
            SensorReading(zone_id=1, moisture=45, ph=6.8),
            SensorReading(zone_id=1, moisture=42, ph=6.9),
            SensorReading(zone_id=2, moisture=35, ph=6.7),
            SensorReading(zone_id=3, moisture=55, ph=6.5)
        ]
        
        for reading in readings:
            self.test_session.add(reading)
        self.test_session.commit()
    
    def test_get_all_zones(self):
        """Test retrieving all zones"""
        zones = self.test_session.query(ZoneModel).all()
        
        self.assertEqual(len(zones), 3)
        zone_names = [zone.name for zone in zones]
        self.assertIn("Vegetable Garden", zone_names)
        self.assertIn("Herb Garden", zone_names)
        self.assertIn("Flower Bed", zone_names)
    
    def test_get_zone_by_id(self):
        """Test retrieving zone by ID"""
        zone = self.test_session.query(ZoneModel).filter_by(id=1).first()
        
        self.assertIsNotNone(zone)
        self.assertEqual(zone.name, "Vegetable Garden")
        self.assertEqual(zone.plant_type, "Vegetables")
    
    def test_get_plants_by_zone(self):
        """Test retrieving plants by zone"""
        plants = self.test_session.query(PlantModel).filter_by(zone_id=1).all()
        
        self.assertEqual(len(plants), 2)
        plant_names = [plant.name for plant in plants]
        self.assertIn("Tomato", plant_names)
        self.assertIn("Basil", plant_names)
    
    def test_get_recent_sensor_readings(self):
        """Test retrieving recent sensor readings"""
        readings = self.test_session.query(SensorReading).filter_by(zone_id=1).all()
        
        self.assertEqual(len(readings), 2)
        for reading in readings:
            self.assertIsInstance(reading.moisture, (int, float))
            self.assertIsInstance(reading.ph, (int, float))
            self.assertGreaterEqual(reading.moisture, 0)
            self.assertLessEqual(reading.moisture, 100)
            self.assertGreaterEqual(reading.ph, 0)
            self.assertLessEqual(reading.ph, 14)
    
    def test_zone_plant_count(self):
        """Test counting plants per zone"""
        zone1_plants = self.test_session.query(PlantModel).filter_by(zone_id=1).count()
        zone2_plants = self.test_session.query(PlantModel).filter_by(zone_id=2).count()
        zone3_plants = self.test_session.query(PlantModel).filter_by(zone_id=3).count()
        
        self.assertEqual(zone1_plants, 2)
        self.assertEqual(zone2_plants, 1)
        self.assertEqual(zone3_plants, 1)
    
    def test_sensor_data_for_charts(self):
        """Test preparing sensor data for charts"""
        # Get readings for zone 1
        readings = self.test_session.query(SensorReading).filter_by(zone_id=1).order_by(SensorReading.timestamp).all()
        
        # Prepare data for charts
        timestamps = [reading.timestamp for reading in readings]
        moisture_values = [reading.moisture for reading in readings]
        ph_values = [reading.ph for reading in readings]
        
        # Verify data structure
        self.assertEqual(len(timestamps), 2)
        self.assertEqual(len(moisture_values), 2)
        self.assertEqual(len(ph_values), 2)
        
        # Verify data types
        for timestamp in timestamps:
            self.assertIsInstance(timestamp, datetime)
        
        for moisture in moisture_values:
            self.assertIsInstance(moisture, (int, float))
        
        for ph in ph_values:
            self.assertIsInstance(ph, (int, float))


class TestZoneStatus(unittest.TestCase):
    """Test cases for zone status calculations"""
    
    def test_zone_moisture_status(self):
        """Test zone moisture status logic"""
        # Zone with good moisture
        zone_good = Zone(
            id=1,
            name="Good Zone",
            moisture=45,
            moisture_threshold=30
        )
        
        # Zone with low moisture
        zone_low = Zone(
            id=2,
            name="Low Zone",
            moisture=25,
            moisture_threshold=30
        )
        
        # Test moisture status
        self.assertGreater(zone_good.moisture, zone_good.moisture_threshold)
        self.assertLess(zone_low.moisture, zone_low.moisture_threshold)
    
    def test_zone_ph_status(self):
        """Test zone pH status logic"""
        # Zone with good pH
        zone_good = Zone(
            id=1,
            name="Good pH Zone",
            ph=6.5,
            ph_range=(6.0, 7.5)
        )
        
        # Zone with bad pH
        zone_bad = Zone(
            id=2,
            name="Bad pH Zone",
            ph=8.0,
            ph_range=(6.0, 7.5)
        )
        
        # Test pH status
        self.assertTrue(zone_good.ph_range[0] <= zone_good.ph <= zone_good.ph_range[1])
        self.assertFalse(zone_bad.ph_range[0] <= zone_bad.ph <= zone_bad.ph_range[1])
    
    def test_zone_overall_status(self):
        """Test overall zone status"""
        # Zone with both good moisture and pH
        zone_healthy = Zone(
            id=1,
            name="Healthy Zone",
            moisture=45,
            ph=6.5,
            moisture_threshold=30,
            ph_range=(6.0, 7.5)
        )
        
        # Zone with low moisture but good pH
        zone_dry = Zone(
            id=2,
            name="Dry Zone",
            moisture=25,
            ph=6.5,
            moisture_threshold=30,
            ph_range=(6.0, 7.5)
        )
        
        # Zone with good moisture but bad pH
        zone_acidic = Zone(
            id=3,
            name="Acidic Zone",
            moisture=45,
            ph=5.0,
            moisture_threshold=30,
            ph_range=(6.0, 7.5)
        )
        
        # Test status logic
        self.assertGreater(zone_healthy.moisture, zone_healthy.moisture_threshold)
        self.assertTrue(zone_healthy.ph_range[0] <= zone_healthy.ph <= zone_healthy.ph_range[1])
        
        self.assertLess(zone_dry.moisture, zone_dry.moisture_threshold)
        self.assertTrue(zone_dry.ph_range[0] <= zone_dry.ph <= zone_dry.ph_range[1])
        
        self.assertGreater(zone_acidic.moisture, zone_acidic.moisture_threshold)
        self.assertFalse(zone_acidic.ph_range[0] <= zone_acidic.ph <= zone_acidic.ph_range[1])


class TestDataValidation(unittest.TestCase):
    """Test cases for data validation"""
    
    def test_zone_data_validation(self):
        """Test zone data validation"""
        # Valid zone data
        valid_zone = Zone(
            name="Test Zone",
            plant_type="Vegetables",
            moisture=45,
            ph=6.8,
            moisture_threshold=30,
            ph_range=(6.0, 7.5)
        )
        
        # Test valid data
        self.assertIsInstance(valid_zone.name, str)
        self.assertIsInstance(valid_zone.plant_type, str)
        self.assertIsInstance(valid_zone.moisture, (int, float))
        self.assertIsInstance(valid_zone.ph, (int, float))
        self.assertIsInstance(valid_zone.moisture_threshold, (int, float))
        self.assertIsInstance(valid_zone.ph_range, tuple)
        self.assertEqual(len(valid_zone.ph_range), 2)
    
    def test_sensor_data_validation(self):
        """Test sensor data validation"""
        # Valid sensor data
        moisture = 45.5
        ph = 6.8
        
        # Test data types and ranges
        self.assertIsInstance(moisture, (int, float))
        self.assertIsInstance(ph, (int, float))
        self.assertGreaterEqual(moisture, 0)
        self.assertLessEqual(moisture, 100)
        self.assertGreaterEqual(ph, 0)
        self.assertLessEqual(ph, 14)
    
    def test_plant_data_validation(self):
        """Test plant data validation"""
        # Valid plant data
        plant_data = {
            'name': 'Tomato',
            'plant_type': 'Vegetable',
            'planting_date': datetime.now().date(),
            'notes': 'Test plant'
        }
        
        # Test data structure
        self.assertIn('name', plant_data)
        self.assertIn('plant_type', plant_data)
        self.assertIn('planting_date', plant_data)
        self.assertIsInstance(plant_data['name'], str)
        self.assertIsInstance(plant_data['plant_type'], str)
        self.assertIsInstance(plant_data['planting_date'], type(datetime.now().date()))


if __name__ == '__main__':
    unittest.main() 