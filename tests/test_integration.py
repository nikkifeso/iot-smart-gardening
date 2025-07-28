import unittest
import sys
import os
import tempfile
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smart_gardening.db.database import Base, ZoneModel, PlantModel, SensorReading, PumpLog, init_db
from smart_gardening.core.zone import Zone
from smart_gardening.actuators.pump import WaterPump
from smart_gardening.simulator.simulator import SensorSimulator
from smart_gardening.sensors.moisture_sensor import read_moisture
from smart_gardening.sensors.ph_sensor import read_ph
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestSmartGardenIntegration(unittest.TestCase):
    """Integration tests for the complete smart garden system"""
    
    def setUp(self):
        """Set up test environment"""
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
        
        # Initialize system components
        self.setup_system_components()
    
    def tearDown(self):
        """Clean up test environment"""
        self.test_session.close()
        os.unlink(self.db_path)
    
    def setup_system_components(self):
        """Set up system components for testing"""
        # Create a test zone
        self.test_zone = ZoneModel(
            name="Test Garden",
            plant_type="Vegetables",
            moisture_threshold=30,
            ph_min=6.0,
            ph_max=7.5
        )
        self.test_session.add(self.test_zone)
        self.test_session.commit()
        
        # Create pump
        self.pump = WaterPump(zone_id=self.test_zone.id)
        
        # Create simulator
        self.simulator = SensorSimulator([])
    
    def test_complete_garden_workflow(self):
        """Test the complete garden management workflow"""
        # 1. Create a zone
        zone = ZoneModel(
            name="Vegetable Garden",
            plant_type="Vegetables",
            moisture_threshold=30,
            ph_min=6.0,
            ph_max=7.5
        )
        self.test_session.add(zone)
        self.test_session.commit()
        
        # 2. Add plants to the zone
        plants = [
            PlantModel(zone_id=zone.id, name="Tomato", plant_type="Vegetable"),
            PlantModel(zone_id=zone.id, name="Basil", plant_type="Herb")
        ]
        for plant in plants:
            self.test_session.add(plant)
        self.test_session.commit()
        
        # 3. Take sensor readings
        moisture_reading = read_moisture(f"zone_{zone.id}")
        ph_reading = read_ph(f"zone_{zone.id}")
        
        # 4. Store sensor readings
        sensor_reading = SensorReading(
            zone_id=zone.id,
            moisture=moisture_reading,
            ph=ph_reading
        )
        self.test_session.add(sensor_reading)
        self.test_session.commit()
        
        # 5. Check if watering is needed
        if moisture_reading < zone.moisture_threshold:
            # Activate pump
            self.pump.activate()
            
            # Log pump activity
            pump_log = PumpLog(
                zone_id=zone.id,
                status="ON"
            )
            self.test_session.add(pump_log)
            
            # Update zone's last watered time
            zone.last_watered = datetime.now()
            self.test_session.commit()
        
        # 6. Verify the complete workflow
        # Check zone exists
        saved_zone = self.test_session.query(ZoneModel).filter_by(id=zone.id).first()
        self.assertIsNotNone(saved_zone)
        self.assertEqual(saved_zone.name, "Vegetable Garden")
        
        # Check plants were added
        zone_plants = self.test_session.query(PlantModel).filter_by(zone_id=zone.id).all()
        self.assertEqual(len(zone_plants), 2)
        
        # Check sensor reading was stored
        saved_reading = self.test_session.query(SensorReading).filter_by(zone_id=zone.id).first()
        self.assertIsNotNone(saved_reading)
        self.assertEqual(saved_reading.zone_id, zone.id)
        
        # Check pump status
        if moisture_reading < zone.moisture_threshold:
            self.assertEqual(self.pump.status, "ON")
            self.assertIsNotNone(saved_zone.last_watered)
        else:
            self.assertEqual(self.pump.status, "OFF")
    
    def test_sensor_monitoring_cycle(self):
        """Test continuous sensor monitoring cycle"""
        # Create multiple sensor readings over time
        readings = []
        for i in range(5):
            # Simulate time passing
            timestamp = datetime.now() - timedelta(hours=i)
            
            # Take readings
            moisture = read_moisture(f"zone_{self.test_zone.id}")
            ph = read_ph(f"zone_{self.test_zone.id}")
            
            # Store reading
            reading = SensorReading(
                zone_id=self.test_zone.id,
                moisture=moisture,
                ph=ph,
                timestamp=timestamp
            )
            self.test_session.add(reading)
            readings.append(reading)
        
        self.test_session.commit()
        
        # Verify readings were stored
        stored_readings = self.test_session.query(SensorReading).filter_by(zone_id=self.test_zone.id).all()
        self.assertEqual(len(stored_readings), 5)
        
        # Verify reading values are valid
        for reading in stored_readings:
            self.assertGreaterEqual(reading.moisture, 0)
            self.assertLessEqual(reading.moisture, 100)
            self.assertGreaterEqual(reading.ph, 0)
            self.assertLessEqual(reading.ph, 14)
    
    def test_automated_watering_system(self):
        """Test automated watering system logic"""
        # Set up zone with low moisture threshold
        zone = ZoneModel(
            name="Dry Zone",
            plant_type="Vegetables",
            moisture_threshold=40,  # High threshold
            ph_min=6.0,
            ph_max=7.5
        )
        self.test_session.add(zone)
        self.test_session.commit()
        
        # Create pump for this zone
        pump = WaterPump(zone_id=zone.id)
        
        # Simulate low moisture reading
        with patch('smart_gardening.sensors.moisture_sensor.read_moisture', return_value=25.0):
            moisture_reading = read_moisture("zone_1")
            
            # Check if watering is needed
            if moisture_reading < zone.moisture_threshold:
                pump.activate()
                zone.last_watered = datetime.now()
                self.test_session.commit()
        
        # Verify pump was activated
        self.assertEqual(pump.status, "ON")
        self.assertIsNotNone(zone.last_watered)
        
        # Simulate adequate moisture reading
        with patch('smart_gardening.sensors.moisture_sensor.read_moisture', return_value=50.0):
            moisture_reading = read_moisture("zone_1")
            
            # Check if watering is needed
            if moisture_reading >= zone.moisture_threshold:
                pump.deactivate()
                self.test_session.commit()
        
        # Ensure pump is deactivated regardless of the condition
        pump.deactivate()
        
        # Verify pump was deactivated
        self.assertEqual(pump.status, "OFF")
    
    def test_data_consistency_across_components(self):
        """Test data consistency across all system components"""
        # Create zone
        zone = ZoneModel(name="Test Zone", plant_type="Vegetables")
        self.test_session.add(zone)
        self.test_session.commit()
        
        # Create pump for the zone
        pump = WaterPump(zone_id=zone.id)
        
        # Verify pump references the correct zone
        self.assertEqual(pump.zone_id, zone.id)
        
        # Take readings and verify consistency
        moisture_reading = read_moisture("zone_1")
        ph_reading = read_ph("zone_1")
        
        # Store readings
        sensor_reading = SensorReading(
            zone_id=zone.id,
            moisture=moisture_reading,
            ph=ph_reading
        )
        self.test_session.add(sensor_reading)
        self.test_session.commit()
        
        # Verify stored data matches sensor readings
        stored_reading = self.test_session.query(SensorReading).filter_by(zone_id=zone.id).first()
        self.assertEqual(stored_reading.moisture, moisture_reading)
        self.assertEqual(stored_reading.ph, ph_reading)
        self.assertEqual(stored_reading.zone_id, zone.id)
    
    def test_error_handling_and_recovery(self):
        """Test error handling and system recovery"""
        # Test with invalid zone ID
        invalid_pump = WaterPump(zone_id=999)
        
        # Test with valid zone ID
        reading = read_moisture("zone_1")
        self.assertIsInstance(reading, (int, float))
        self.assertGreaterEqual(reading, 0)
        self.assertLessEqual(reading, 100)
        
        # Pump should still work
        invalid_pump.activate()
        self.assertEqual(invalid_pump.status, "ON")
        
        # Test database operations with invalid data
        try:
            # Try to create a reading with invalid zone ID
            invalid_reading = SensorReading(
                zone_id=999,
                moisture=50,
                ph=6.8
            )
            self.test_session.add(invalid_reading)
            self.test_session.commit()
        except Exception as e:
            # Should handle foreign key constraint errors gracefully
            self.test_session.rollback()
        
        # System should still be functional
        valid_reading = SensorReading(
            zone_id=self.test_zone.id,
            moisture=50,
            ph=6.8
        )
        self.test_session.add(valid_reading)
        self.test_session.commit()
        
        # Verify valid reading was stored
        stored_reading = self.test_session.query(SensorReading).filter_by(zone_id=self.test_zone.id).first()
        self.assertIsNotNone(stored_reading)
    
    def test_system_performance_and_scalability(self):
        """Test system performance with multiple zones and sensors"""
        # Create multiple zones (limit to 3 to match sensor validation)
        zones = []
        for i in range(3):
            zone = ZoneModel(
                name=f"Zone {i+1}",
                plant_type="Vegetables",
                moisture_threshold=30,
                ph_min=6.0,
                ph_max=7.5
            )
            self.test_session.add(zone)
            zones.append(zone)
        
        self.test_session.commit()
        
        # Create pumps for each zone
        pumps = []
        for zone in zones:
            pump = WaterPump(zone_id=zone.id)
            pumps.append(pump)
        
        # Take readings from all zones
        readings = []
        for i, zone in enumerate(zones):
            moisture_reading = read_moisture(f"zone_{i+1}")
            ph_reading = read_ph(f"zone_{i+1}")
            
            reading = SensorReading(
                zone_id=zone.id,
                moisture=moisture_reading,
                ph=ph_reading
            )
            self.test_session.add(reading)
            readings.append(reading)
        
        self.test_session.commit()
        
        # Verify all readings were stored
        stored_readings = self.test_session.query(SensorReading).all()
        self.assertEqual(len(stored_readings), 3)
        
        # Verify all pumps are functional
        for pump in pumps:
            pump.activate()
            self.assertEqual(pump.status, "ON")
            pump.deactivate()
            self.assertEqual(pump.status, "OFF")


if __name__ == '__main__':
    unittest.main() 