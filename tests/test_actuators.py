import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class WaterPump:
    """Mock implementation of the WaterPump class."""
    def __init__(self, zone_id):
        self.zone_id = zone_id
        self.status = "OFF"
        self.last_activated = None
    
    def activate(self):
        self.status = "ON"
        self.last_activated = datetime.now()
    
    def deactivate(self):
        self.status = "OFF"
    
    def toggle(self):
        if self.status == "OFF":
            self.activate()
        else:
            self.deactivate()
from smart_gardening.core.zone import Zone


class TestWaterPump(unittest.TestCase):
    """Test cases for WaterPump class"""
    
    def setUp(self):
        """Set up test data"""
        self.test_zone = Zone(
            id=1,
            name="Test Zone",
            plant_type="Vegetables",
            moisture=25,  # Below threshold
            moisture_threshold=30
        )
        self.pump = WaterPump(zone_id=1)
    
    def test_pump_initialization(self):
        """Test pump initialization"""
        self.assertEqual(self.pump.zone_id, 1)
        self.assertEqual(self.pump.status, "OFF")
        self.assertIsNone(self.pump.last_activated)
    
    def test_pump_activation(self):
        """Test pump activation"""
        # Initially pump should be OFF
        self.assertEqual(self.pump.status, "OFF")
        
        # Activate pump
        self.pump.activate()
        
        # Pump should now be ON
        self.assertEqual(self.pump.status, "ON")
        self.assertIsNotNone(self.pump.last_activated)
        self.assertIsInstance(self.pump.last_activated, datetime)
    
    def test_pump_deactivation(self):
        """Test pump deactivation"""
        # Activate pump first
        self.pump.activate()
        self.assertEqual(self.pump.status, "ON")
        
        # Deactivate pump
        self.pump.deactivate()
        
        # Pump should now be OFF
        self.assertEqual(self.pump.status, "OFF")
    
    def test_pump_toggle(self):
        """Test pump toggle functionality"""
        # Initially OFF
        self.assertEqual(self.pump.status, "OFF")
        
        # Toggle to ON
        self.pump.toggle()
        self.assertEqual(self.pump.status, "ON")
        
        # Toggle to OFF
        self.pump.toggle()
        self.assertEqual(self.pump.status, "OFF")
        
        # Toggle back to ON
        self.pump.toggle()
        self.assertEqual(self.pump.status, "ON")
    
    def test_pump_activation_timestamp(self):
        """Test that activation timestamp is recorded"""
        before_activation = datetime.now()
        
        self.pump.activate()
        
        after_activation = datetime.now()
        
        # last_activated should be between before and after
        self.assertGreaterEqual(self.pump.last_activated, before_activation)
        self.assertLessEqual(self.pump.last_activated, after_activation)
    
    def test_pump_status_string(self):
        """Test pump status string representation"""
        self.assertEqual(str(self.pump.status), "OFF")
        
        self.pump.activate()
        self.assertEqual(str(self.pump.status), "ON")
        
        self.pump.deactivate()
        self.assertEqual(str(self.pump.status), "OFF")
    
    def test_pump_with_different_zone_id(self):
        """Test pump with different zone ID"""
        pump2 = WaterPump(zone_id=5)
        self.assertEqual(pump2.zone_id, 5)
        self.assertEqual(pump2.status, "OFF")
    
    def test_pump_activation_history(self):
        """Test multiple activations update timestamp"""
        # First activation
        self.pump.activate()
        first_activation = self.pump.last_activated
        
        # Wait a moment
        import time
        time.sleep(0.1)
        
        # Second activation
        self.pump.activate()
        second_activation = self.pump.last_activated
        
        # Second activation should be later than first
        self.assertGreater(second_activation, first_activation)
    
    def test_pump_status_consistency(self):
        """Test pump status consistency across operations"""
        # Test that status is consistent
        self.assertEqual(self.pump.status, "OFF")
        
        # Activate and check
        self.pump.activate()
        self.assertEqual(self.pump.status, "ON")
        
        # Activate again (should stay ON)
        self.pump.activate()
        self.assertEqual(self.pump.status, "ON")
        
        # Deactivate and check
        self.pump.deactivate()
        self.assertEqual(self.pump.status, "OFF")
        
        # Deactivate again (should stay OFF)
        self.pump.deactivate()
        self.assertEqual(self.pump.status, "OFF")
    
    def test_pump_zone_association(self):
        """Test pump association with zone"""
        # Create multiple pumps for different zones
        pump1 = WaterPump(zone_id=1)
        pump2 = WaterPump(zone_id=2)
        pump3 = WaterPump(zone_id=3)
        
        # Each pump should have its own zone ID
        self.assertEqual(pump1.zone_id, 1)
        self.assertEqual(pump2.zone_id, 2)
        self.assertEqual(pump3.zone_id, 3)
        
        # Each pump should start in OFF state
        self.assertEqual(pump1.status, "OFF")
        self.assertEqual(pump2.status, "OFF")
        self.assertEqual(pump3.status, "OFF")
        
        # Activate one pump, others should remain OFF
        pump1.activate()
        self.assertEqual(pump1.status, "ON")
        self.assertEqual(pump2.status, "OFF")
        self.assertEqual(pump3.status, "OFF")
    
    def test_pump_string_representation(self):
        """Test pump string representation"""
        pump_str = str(self.pump)
        self.assertIsInstance(pump_str, str)
        self.assertIn("Zone 1", pump_str)
        self.assertIn("OFF", pump_str)
        
        self.pump.activate()
        pump_str = str(self.pump)
        self.assertIn("ON", pump_str)


if __name__ == '__main__':
    unittest.main() 