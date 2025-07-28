import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smart_gardening.sensors.moisture_sensor import MoistureSensor
from smart_gardening.sensors.ph_sensor import PHSensor


class TestMoistureSensor(unittest.TestCase):
    """Test cases for MoistureSensor class"""
    
    def setUp(self):
        """Set up test data"""
        self.sensor = MoistureSensor(zone_id=1)
    
    def test_sensor_initialization(self):
        """Test sensor initialization"""
        self.assertEqual(self.sensor.zone_id, 1)
        self.assertIsInstance(self.sensor.current_reading, (int, float))
        self.assertGreaterEqual(self.sensor.current_reading, 0)
        self.assertLessEqual(self.sensor.current_reading, 100)
    
    def test_read_moisture(self):
        """Test moisture reading"""
        reading = self.sensor.read()
        
        # Reading should be a valid moisture percentage
        self.assertIsInstance(reading, (int, float))
        self.assertGreaterEqual(reading, 0)
        self.assertLessEqual(reading, 100)
        
        # Current reading should be updated
        self.assertEqual(self.sensor.current_reading, reading)
    
    def test_multiple_readings(self):
        """Test multiple moisture readings"""
        readings = []
        
        for _ in range(5):
            reading = self.sensor.read()
            readings.append(reading)
        
        # All readings should be valid
        for reading in readings:
            self.assertIsInstance(reading, (int, float))
            self.assertGreaterEqual(reading, 0)
            self.assertLessEqual(reading, 100)
        
        # Current reading should be the last one
        self.assertEqual(self.sensor.current_reading, readings[-1])
    
    def test_sensor_with_different_zone_id(self):
        """Test sensor with different zone ID"""
        sensor2 = MoistureSensor(zone_id=5)
        self.assertEqual(sensor2.zone_id, 5)
    
    def test_sensor_reading_realistic_values(self):
        """Test that sensor readings are realistic for soil moisture"""
        reading = self.sensor.read()
        
        # Soil moisture should typically be between 10% and 90%
        self.assertGreaterEqual(reading, 10)
        self.assertLessEqual(reading, 90)
    
    @patch('random.uniform')
    def test_sensor_with_mocked_random(self, mock_uniform):
        """Test sensor with mocked random values"""
        # Mock random value
        mock_uniform.return_value = 45.5
        
        reading = self.sensor.read()
        
        # Check that random.uniform was called
        self.assertTrue(mock_uniform.called)
        
        # Reading should be the mocked value
        self.assertEqual(reading, 45.5)
        self.assertEqual(self.sensor.current_reading, 45.5)
    
    def test_sensor_string_representation(self):
        """Test sensor string representation"""
        sensor_str = str(self.sensor)
        self.assertIsInstance(sensor_str, str)
        self.assertIn("Zone 1", sensor_str)
        self.assertIn("Moisture", sensor_str)


class TestPHSensor(unittest.TestCase):
    """Test cases for PHSensor class"""
    
    def setUp(self):
        """Set up test data"""
        self.sensor = PHSensor(zone_id=1)
    
    def test_sensor_initialization(self):
        """Test sensor initialization"""
        self.assertEqual(self.sensor.zone_id, 1)
        self.assertIsInstance(self.sensor.current_reading, (int, float))
        self.assertGreaterEqual(self.sensor.current_reading, 0)
        self.assertLessEqual(self.sensor.current_reading, 14)
    
    def test_read_ph(self):
        """Test pH reading"""
        reading = self.sensor.read()
        
        # Reading should be a valid pH value
        self.assertIsInstance(reading, (int, float))
        self.assertGreaterEqual(reading, 0)
        self.assertLessEqual(reading, 14)
        
        # Current reading should be updated
        self.assertEqual(self.sensor.current_reading, reading)
    
    def test_multiple_readings(self):
        """Test multiple pH readings"""
        readings = []
        
        for _ in range(5):
            reading = self.sensor.read()
            readings.append(reading)
        
        # All readings should be valid
        for reading in readings:
            self.assertIsInstance(reading, (int, float))
            self.assertGreaterEqual(reading, 0)
            self.assertLessEqual(reading, 14)
        
        # Current reading should be the last one
        self.assertEqual(self.sensor.current_reading, readings[-1])
    
    def test_sensor_with_different_zone_id(self):
        """Test sensor with different zone ID"""
        sensor2 = PHSensor(zone_id=5)
        self.assertEqual(sensor2.zone_id, 5)
    
    def test_sensor_reading_realistic_values(self):
        """Test that sensor readings are realistic for soil pH"""
        reading = self.sensor.read()
        
        # Soil pH should typically be between 5.0 and 8.5
        self.assertGreaterEqual(reading, 5.0)
        self.assertLessEqual(reading, 8.5)
    
    @patch('random.uniform')
    def test_sensor_with_mocked_random(self, mock_uniform):
        """Test sensor with mocked random values"""
        # Mock random value
        mock_uniform.return_value = 6.8
        
        reading = self.sensor.read()
        
        # Check that random.uniform was called
        self.assertTrue(mock_uniform.called)
        
        # Reading should be the mocked value
        self.assertEqual(reading, 6.8)
        self.assertEqual(self.sensor.current_reading, 6.8)
    
    def test_sensor_string_representation(self):
        """Test sensor string representation"""
        sensor_str = str(self.sensor)
        self.assertIsInstance(sensor_str, str)
        self.assertIn("Zone 1", sensor_str)
        self.assertIn("pH", sensor_str)
    
    def test_ph_scale_boundaries(self):
        """Test pH scale boundaries"""
        # Test that pH values are within the valid scale (0-14)
        for _ in range(10):
            reading = self.sensor.read()
            self.assertGreaterEqual(reading, 0)
            self.assertLessEqual(reading, 14)


class TestSensorIntegration(unittest.TestCase):
    """Test cases for sensor integration"""
    
    def test_multiple_sensors_same_zone(self):
        """Test multiple sensors in the same zone"""
        moisture_sensor = MoistureSensor(zone_id=1)
        ph_sensor = PHSensor(zone_id=1)
        
        # Both sensors should have the same zone_id
        self.assertEqual(moisture_sensor.zone_id, 1)
        self.assertEqual(ph_sensor.zone_id, 1)
        
        # Both should be able to read independently
        moisture_reading = moisture_sensor.read()
        ph_reading = ph_sensor.read()
        
        self.assertIsInstance(moisture_reading, (int, float))
        self.assertIsInstance(ph_reading, (int, float))
        
        # Readings should be in appropriate ranges
        self.assertGreaterEqual(moisture_reading, 0)
        self.assertLessEqual(moisture_reading, 100)
        self.assertGreaterEqual(ph_reading, 0)
        self.assertLessEqual(ph_reading, 14)
    
    def test_sensors_different_zones(self):
        """Test sensors in different zones"""
        moisture_sensor1 = MoistureSensor(zone_id=1)
        moisture_sensor2 = MoistureSensor(zone_id=2)
        ph_sensor1 = PHSensor(zone_id=1)
        ph_sensor2 = PHSensor(zone_id=2)
        
        # Sensors should have correct zone IDs
        self.assertEqual(moisture_sensor1.zone_id, 1)
        self.assertEqual(moisture_sensor2.zone_id, 2)
        self.assertEqual(ph_sensor1.zone_id, 1)
        self.assertEqual(ph_sensor2.zone_id, 2)
        
        # All sensors should be able to read
        readings = [
            moisture_sensor1.read(),
            moisture_sensor2.read(),
            ph_sensor1.read(),
            ph_sensor2.read()
        ]
        
        for reading in readings:
            self.assertIsInstance(reading, (int, float))


if __name__ == '__main__':
    unittest.main() 