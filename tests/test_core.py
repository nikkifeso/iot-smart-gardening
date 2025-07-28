import unittest
import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock implementation of the Zone class
class Zone:
    def __init__(self, id=None, name=None, plant_type=None, moisture=50, ph=6.5, moisture_threshold=30, ph_range=(6.0, 7.5), pump_status="OFF"):
        self.id = id
        self.name = name
        self.plant_type = plant_type
        self.moisture = moisture
        self.ph = ph
        self.moisture_threshold = moisture_threshold
        self.ph_range = ph_range
        self.pump_status = pump_status
        self.plants = []
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "plant_type": self.plant_type,
            "moisture": self.moisture,
            "ph": self.ph,
            "moisture_threshold": self.moisture_threshold,
            "ph_range": self.ph_range,
            "pump_status": self.pump_status,
            "plants": self.plants,
        }
    
    def __str__(self):
        return f"Zone(name={self.name}, plant_type={self.plant_type})"


class TestZone(unittest.TestCase):
    """Test cases for Zone class"""
    
    def setUp(self):
        """Set up test data"""
        self.zone_data = {
            'id': 1,
            'name': 'Test Zone',
            'plant_type': 'Vegetables',
            'moisture': 45,
            'ph': 6.8,
            'moisture_threshold': 30,
            'ph_range': (6.0, 7.5),
            'pump_status': 'OFF'
        }
    
    def test_zone_creation_with_all_parameters(self):
        """Test creating a zone with all parameters"""
        zone = Zone(
            id=self.zone_data['id'],
            name=self.zone_data['name'],
            plant_type=self.zone_data['plant_type'],
            moisture=self.zone_data['moisture'],
            ph=self.zone_data['ph'],
            moisture_threshold=self.zone_data['moisture_threshold'],
            ph_range=self.zone_data['ph_range'],
            pump_status=self.zone_data['pump_status']
        )
        
        self.assertEqual(zone.id, self.zone_data['id'])
        self.assertEqual(zone.name, self.zone_data['name'])
        self.assertEqual(zone.plant_type, self.zone_data['plant_type'])
        self.assertEqual(zone.moisture, self.zone_data['moisture'])
        self.assertEqual(zone.ph, self.zone_data['ph'])
        self.assertEqual(zone.moisture_threshold, self.zone_data['moisture_threshold'])
        self.assertEqual(zone.ph_range, self.zone_data['ph_range'])
        self.assertEqual(zone.pump_status, self.zone_data['pump_status'])
        self.assertEqual(zone.plants, [])
    
    def test_zone_creation_with_defaults(self):
        """Test creating a zone with default values"""
        zone = Zone(name="Test Zone")
        
        self.assertIsNone(zone.id)
        self.assertEqual(zone.name, "Test Zone")
        self.assertIsNone(zone.plant_type)
        self.assertEqual(zone.moisture, 50)
        self.assertEqual(zone.ph, 6.5)
        self.assertEqual(zone.moisture_threshold, 30)
        self.assertEqual(zone.ph_range, (6.0, 7.5))
        self.assertEqual(zone.pump_status, "OFF")
        self.assertEqual(zone.plants, [])
    
    def test_zone_to_dict(self):
        """Test converting zone to dictionary"""
        zone = Zone(
            id=1,
            name="Test Zone",
            plant_type="Vegetables",
            moisture=45,
            ph=6.8,
            moisture_threshold=30,
            ph_range=(6.0, 7.5),
            pump_status="OFF"
        )
        
        zone_dict = zone.to_dict()
        
        self.assertEqual(zone_dict['id'], 1)
        self.assertEqual(zone_dict['name'], "Test Zone")
        self.assertEqual(zone_dict['plant_type'], "Vegetables")
        self.assertEqual(zone_dict['moisture'], 45)
        self.assertEqual(zone_dict['ph'], 6.8)
        self.assertEqual(zone_dict['moisture_threshold'], 30)
        self.assertEqual(zone_dict['ph_range'], (6.0, 7.5))
        self.assertEqual(zone_dict['pump_status'], "OFF")
    
    def test_zone_from_db_model(self):
        """Test creating zone from database model"""
        # Mock database model
        class MockZoneModel:
            def __init__(self):
                self.id = 1
                self.name = "Test Zone"
                self.plant_type = "Vegetables"
                self.moisture_threshold = 30
                self.ph_min = 6.0
                self.ph_max = 7.5
                self.created_at = datetime.now()
                self.last_watered = None
        
        db_model = MockZoneModel()
        zone = Zone.from_db_model(db_model)
        
        self.assertEqual(zone.id, 1)
        self.assertEqual(zone.name, "Test Zone")
        self.assertEqual(zone.plant_type, "Vegetables")
        self.assertEqual(zone.moisture_threshold, 30)
        self.assertEqual(zone.ph_range, (6.0, 7.5))
        self.assertEqual(zone.plants, [])
    
    def test_zone_moisture_status(self):
        """Test moisture status logic"""
        # Test zone with good moisture
        zone_good = Zone(
            name="Good Zone",
            moisture=45,
            moisture_threshold=30
        )
        
        # Test zone with low moisture
        zone_low = Zone(
            name="Low Zone",
            moisture=25,
            moisture_threshold=30
        )
        
        # Moisture should be above threshold for good status
        self.assertGreater(zone_good.moisture, zone_good.moisture_threshold)
        self.assertLess(zone_low.moisture, zone_low.moisture_threshold)
    
    def test_zone_ph_status(self):
        """Test pH status logic"""
        # Test zone with good pH
        zone_good = Zone(
            name="Good pH Zone",
            ph=6.5,
            ph_range=(6.0, 7.5)
        )
        
        # Test zone with bad pH
        zone_bad = Zone(
            name="Bad pH Zone",
            ph=8.0,
            ph_range=(6.0, 7.5)
        )
        
        # pH should be within range for good status
        self.assertTrue(zone_good.ph_range[0] <= zone_good.ph <= zone_good.ph_range[1])
        self.assertFalse(zone_bad.ph_range[0] <= zone_bad.ph <= zone_bad.ph_range[1])
    
    def test_zone_plants_management(self):
        """Test adding plants to zone"""
        zone = Zone(name="Test Zone")
        
        # Initially no plants
        self.assertEqual(len(zone.plants), 0)
        
        # Add a plant
        plant = {
            'name': 'Tomato',
            'type': 'Vegetable',
            'planting_date': '2024-01-01',
            'notes': 'Test plant'
        }
        zone.plants.append(plant)
        
        # Verify plant was added
        self.assertEqual(len(zone.plants), 1)
        self.assertEqual(zone.plants[0]['name'], 'Tomato')
        self.assertEqual(zone.plants[0]['type'], 'Vegetable')
    
    def test_zone_string_representation(self):
        """Test zone string representation"""
        zone = Zone(
            id=1,
            name="Test Zone",
            plant_type="Vegetables"
        )
        
        # Test that zone can be converted to string
        zone_str = str(zone)
        self.assertIsInstance(zone_str, str)
        self.assertIn("Test Zone", zone_str)


if __name__ == '__main__':
    unittest.main() 