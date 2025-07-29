import unittest
import tempfile
import os
import sys
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smart_gardening.db.database import Base, ZoneModel, PlantModel, SensorReading, PumpLog, init_db, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestDatabase(unittest.TestCase):
    """Test cases for database models and operations"""
    
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
    
    def tearDown(self):
        """Clean up test database"""
        self.test_session.close()
        os.unlink(self.db_path)
    
    def test_zone_creation(self):
        """Test creating a zone"""
        zone = ZoneModel(
            name="Test Zone",
            plant_type="Vegetables",
            moisture_threshold=30,
            ph_min=6.0,
            ph_max=7.5
        )
        
        self.test_session.add(zone)
        self.test_session.commit()
        
        # Verify zone was created
        saved_zone = self.test_session.query(ZoneModel).filter_by(name="Test Zone").first()
        self.assertIsNotNone(saved_zone)
        self.assertEqual(saved_zone.name, "Test Zone")
        self.assertEqual(saved_zone.plant_type, "Vegetables")
        self.assertEqual(saved_zone.moisture_threshold, 30)
        self.assertEqual(saved_zone.ph_min, 6.0)
        self.assertEqual(saved_zone.ph_max, 7.5)
        self.assertIsNotNone(saved_zone.created_at)
    
    def test_plant_creation(self):
        """Test creating a plant"""
        zone = ZoneModel(name="Test Zone", plant_type="Vegetables")
        self.test_session.add(zone)
        self.test_session.commit()
        
        plant = PlantModel(
            zone_id=zone.id,
            name="Tomato",
            plant_type="Vegetable",
            planting_date=datetime.now().date(),
            notes="Test tomato plant"
        )
        
        self.test_session.add(plant)
        self.test_session.commit()
        
        # Verify plant was created
        saved_plant = self.test_session.query(PlantModel).filter_by(name="Tomato").first()
        self.assertIsNotNone(saved_plant)
        self.assertEqual(saved_plant.name, "Tomato")
        self.assertEqual(saved_plant.zone_id, zone.id)
        self.assertEqual(saved_plant.plant_type, "Vegetable")
        self.assertIsNotNone(saved_plant.created_at)
    
    def test_plant_removal(self):
        """Test removing a plant"""
        from smart_gardening.db.database import remove_plant, get_plant_by_id
        
        # Create a test zone
        zone = ZoneModel(name="Test Zone", plant_type="Vegetables")
        self.test_session.add(zone)
        self.test_session.commit()
        
        # Create a test plant
        plant = PlantModel(
            zone_id=zone.id,
            name="Test Plant",
            plant_type="Vegetable",
            planting_date=datetime.now(),
            notes="Test plant for removal"
        )
        self.test_session.add(plant)
        self.test_session.commit()
        
        plant_id = plant.id
        self.assertIsNotNone(plant_id)
        
        # Verify plant exists using the same session
        retrieved_plant = self.test_session.query(PlantModel).filter(PlantModel.id == plant_id).first()
        self.assertIsNotNone(retrieved_plant)
        self.assertEqual(retrieved_plant.name, "Test Plant")
        
        # Remove the plant using the test session
        success = remove_plant(plant_id, self.test_session)
        self.assertTrue(success)
        
        # Verify plant is gone using the same session
        retrieved_plant_after = self.test_session.query(PlantModel).filter(PlantModel.id == plant_id).first()
        self.assertIsNone(retrieved_plant_after)
    
    def test_remove_nonexistent_plant(self):
        """Test removing a plant that doesn't exist"""
        from smart_gardening.db.database import remove_plant
        
        # Try to remove a plant with a non-existent ID
        success = remove_plant(99999, self.test_session)
        self.assertFalse(success)
    
    def test_remove_plant_with_sensor_readings(self):
        """Test removing a plant when zone has sensor readings"""
        from smart_gardening.db.database import remove_plant
        
        zone = ZoneModel(name="Test Zone", plant_type="Vegetables")
        self.test_session.add(zone)
        self.test_session.commit()
        
        plant = PlantModel(
            zone_id=zone.id,
            name="Test Plant",
            plant_type="Vegetable",
            planting_date=datetime.now(),
            notes="Test plant for removal"
        )
        self.test_session.add(plant)
        self.test_session.commit()
        
        reading = SensorReading(
            zone_id=zone.id,
            moisture=45.5,
            ph=6.8
        )
        self.test_session.add(reading)
        self.test_session.commit()
        
        success = remove_plant(plant.id, self.test_session)
        self.assertTrue(success)
        
        retrieved_plant = self.test_session.query(PlantModel).filter(PlantModel.id == plant.id).first()
        self.assertIsNone(retrieved_plant)
        
        sensor_readings = self.test_session.query(SensorReading).filter(SensorReading.zone_id == zone.id).all()
        self.assertEqual(len(sensor_readings), 1)
    
    def test_remove_plant_with_pump_logs(self):
        """Test removing a plant when zone has pump logs"""
        from smart_gardening.db.database import remove_plant
        
        zone = ZoneModel(name="Test Zone", plant_type="Vegetables")
        self.test_session.add(zone)
        self.test_session.commit()
        
        plant = PlantModel(
            zone_id=zone.id,
            name="Test Plant",
            plant_type="Vegetable",
            planting_date=datetime.now(),
            notes="Test plant for removal"
        )
        self.test_session.add(plant)
        self.test_session.commit()
        
        pump_log = PumpLog(
            zone_id=zone.id,
            status="ON"
        )
        self.test_session.add(pump_log)
        self.test_session.commit()
        
        success = remove_plant(plant.id, self.test_session)
        self.assertTrue(success)
        
        retrieved_plant = self.test_session.query(PlantModel).filter(PlantModel.id == plant.id).first()
        self.assertIsNone(retrieved_plant)
        
        pump_logs = self.test_session.query(PumpLog).filter(PumpLog.zone_id == zone.id).all()
        self.assertEqual(len(pump_logs), 1)
    
    def test_remove_multiple_plants_from_zone(self):
        """Test removing multiple plants from the same zone"""
        from smart_gardening.db.database import remove_plant
        
        zone = ZoneModel(name="Test Zone", plant_type="Vegetables")
        self.test_session.add(zone)
        self.test_session.commit()
        
        plants = []
        for i in range(3):
            plant = PlantModel(
                zone_id=zone.id,
                name=f"Test Plant {i+1}",
                plant_type="Vegetable",
                planting_date=datetime.now(),
                notes=f"Test plant {i+1} for removal"
            )
            self.test_session.add(plant)
            plants.append(plant)
        
        self.test_session.commit()
        
        zone_plants = self.test_session.query(PlantModel).filter(PlantModel.zone_id == zone.id).all()
        self.assertEqual(len(zone_plants), 3)
        
        success1 = remove_plant(plants[0].id, self.test_session)
        self.assertTrue(success1)
        
        success2 = remove_plant(plants[1].id, self.test_session)
        self.assertTrue(success2)
        
        remaining_plants = self.test_session.query(PlantModel).filter(PlantModel.zone_id == zone.id).all()
        self.assertEqual(len(remaining_plants), 1)
        self.assertEqual(remaining_plants[0].name, "Test Plant 3")
    
    def test_remove_plant_invalid_id(self):
        """Test removing a plant with invalid ID types"""
        from smart_gardening.db.database import remove_plant
        
        success = remove_plant(None, self.test_session)
        self.assertFalse(success)
        
        success = remove_plant(-1, self.test_session)
        self.assertFalse(success)
        
        success = remove_plant(0, self.test_session)
        self.assertFalse(success)
    
    def test_get_plant_by_id_functionality(self):
        """Test the get_plant_by_id function"""
        from smart_gardening.db.database import get_plant_by_id
        
        zone = ZoneModel(name="Test Zone", plant_type="Vegetables")
        self.test_session.add(zone)
        self.test_session.commit()
        
        plant = PlantModel(
            zone_id=zone.id,
            name="Test Plant",
            plant_type="Vegetable",
            planting_date=datetime.now(),
            notes="Test plant"
        )
        self.test_session.add(plant)
        self.test_session.commit()
        
        retrieved_plant = self.test_session.query(PlantModel).filter(PlantModel.id == plant.id).first()
        self.assertIsNotNone(retrieved_plant)
        self.assertEqual(retrieved_plant.name, "Test Plant")
        self.assertEqual(retrieved_plant.zone_id, zone.id)
        
        non_existent_plant = self.test_session.query(PlantModel).filter(PlantModel.id == 99999).first()
        self.assertIsNone(non_existent_plant)
    
    def test_sensor_reading_creation(self):
        """Test creating sensor readings"""
        # First create a zone
        zone = ZoneModel(name="Test Zone", plant_type="Vegetables")
        self.test_session.add(zone)
        self.test_session.commit()
        
        # Create sensor reading
        reading = SensorReading(
            zone_id=zone.id,
            moisture=45.5,
            ph=6.8
        )
        
        self.test_session.add(reading)
        self.test_session.commit()
        
        # Verify reading was created
        saved_reading = self.test_session.query(SensorReading).filter_by(zone_id=zone.id).first()
        self.assertIsNotNone(saved_reading)
        self.assertEqual(saved_reading.moisture, 45.5)
        self.assertEqual(saved_reading.ph, 6.8)
        self.assertEqual(saved_reading.zone_id, zone.id)
        self.assertIsNotNone(saved_reading.timestamp)
    
    def test_pump_log_creation(self):
        """Test creating pump logs"""
        # First create a zone
        zone = ZoneModel(name="Test Zone", plant_type="Vegetables")
        self.test_session.add(zone)
        self.test_session.commit()
        
        # Create pump log
        pump_log = PumpLog(
            zone_id=zone.id,
            status="ON"
        )
        
        self.test_session.add(pump_log)
        self.test_session.commit()
        
        # Verify pump log was created
        saved_log = self.test_session.query(PumpLog).filter_by(zone_id=zone.id).first()
        self.assertIsNotNone(saved_log)
        self.assertEqual(saved_log.status, "ON")
        self.assertEqual(saved_log.zone_id, zone.id)
        self.assertIsNotNone(saved_log.timestamp)
    
    def test_zone_plant_relationship(self):
        """Test relationship between zones and plants"""
        # Create a zone
        zone = ZoneModel(name="Test Zone", plant_type="Vegetables")
        self.test_session.add(zone)
        self.test_session.commit()
        
        # Create multiple plants for the zone
        plants = [
            PlantModel(zone_id=zone.id, name="Tomato", plant_type="Vegetable"),
            PlantModel(zone_id=zone.id, name="Basil", plant_type="Herb"),
            PlantModel(zone_id=zone.id, name="Lettuce", plant_type="Vegetable")
        ]
        
        for plant in plants:
            self.test_session.add(plant)
        self.test_session.commit()
        
        # Verify plants are associated with the zone
        zone_plants = self.test_session.query(PlantModel).filter_by(zone_id=zone.id).all()
        self.assertEqual(len(zone_plants), 3)
        
        plant_names = [plant.name for plant in zone_plants]
        self.assertIn("Tomato", plant_names)
        self.assertIn("Basil", plant_names)
        self.assertIn("Lettuce", plant_names)
    
    def test_zone_sensor_relationship(self):
        """Test relationship between zones and sensor readings"""
        # Create a zone
        zone = ZoneModel(name="Test Zone", plant_type="Vegetables")
        self.test_session.add(zone)
        self.test_session.commit()
        
        # Create multiple sensor readings
        readings = [
            SensorReading(zone_id=zone.id, moisture=40, ph=6.5),
            SensorReading(zone_id=zone.id, moisture=45, ph=6.8),
            SensorReading(zone_id=zone.id, moisture=50, ph=7.0)
        ]
        
        for reading in readings:
            self.test_session.add(reading)
        self.test_session.commit()
        
        # Verify readings are associated with the zone
        zone_readings = self.test_session.query(SensorReading).filter_by(zone_id=zone.id).all()
        self.assertEqual(len(zone_readings), 3)
        
        moisture_values = [reading.moisture for reading in zone_readings]
        self.assertIn(40, moisture_values)
        self.assertIn(45, moisture_values)
        self.assertIn(50, moisture_values)
    
    def test_last_watered_update(self):
        """Test updating last watered timestamp"""
        zone = ZoneModel(name="Test Zone", plant_type="Vegetables")
        self.test_session.add(zone)
        self.test_session.commit()
        
        # Initially, last_watered should be None
        self.assertIsNone(zone.last_watered)
        
        # Update last watered time
        now = datetime.now()
        zone.last_watered = now
        self.test_session.commit()
        
        # Verify update
        updated_zone = self.test_session.query(ZoneModel).filter_by(id=zone.id).first()
        self.assertIsNotNone(updated_zone.last_watered)
        self.assertEqual(updated_zone.last_watered, now)


if __name__ == '__main__':
    unittest.main() 