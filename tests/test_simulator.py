import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smart_gardening.simulator.simulator import SensorSimulator
from smart_gardening.core.zone import Zone


class TestSensorSimulator(unittest.TestCase):
    """Test cases for SensorSimulator class"""
    
    def setUp(self):
        """Set up test data"""
        self.test_zones = [
            Zone(id=1, name="Zone 1", plant_type="Vegetables", moisture=45, ph=6.8),
            Zone(id=2, name="Zone 2", plant_type="Herbs", moisture=35, ph=7.2),
            Zone(id=3, name="Zone 3", plant_type="Flowers", moisture=55, ph=6.5)
        ]
        self.simulator = SensorSimulator(self.test_zones)
    
    def test_simulator_initialization(self):
        """Test simulator initialization"""
        self.assertEqual(len(self.simulator.zones), 3)
        self.assertEqual(self.simulator.zones[0].name, "Zone 1")
        self.assertEqual(self.simulator.zones[1].name, "Zone 2")
        self.assertEqual(self.simulator.zones[2].name, "Zone 3")
    
    def test_simulate_moisture_changes(self):
        """Test moisture simulation"""
        initial_moisture = self.simulator.zones[0].moisture
        
        # Simulate moisture changes
        self.simulator.simulate()
        
        # Moisture should change (either increase or decrease)
        new_moisture = self.simulator.zones[0].moisture
        self.assertIsInstance(new_moisture, (int, float))
        self.assertGreaterEqual(new_moisture, 0)
        self.assertLessEqual(new_moisture, 100)
    
    def test_simulate_ph_changes(self):
        """Test pH simulation"""
        initial_ph = self.simulator.zones[0].ph
        
        # Simulate pH changes
        self.simulator.simulate()
        
        # pH should change within reasonable bounds
        new_ph = self.simulator.zones[0].ph
        self.assertIsInstance(new_ph, (int, float))
        self.assertGreaterEqual(new_ph, 0)
        self.assertLessEqual(new_ph, 14)
    
    def test_simulate_all_zones(self):
        """Test that all zones are simulated"""
        initial_moistures = [zone.moisture for zone in self.simulator.zones]
        initial_phs = [zone.ph for zone in self.simulator.zones]
        
        # Simulate all zones
        self.simulator.simulate()
        
        # Check that all zones have been updated
        for i, zone in enumerate(self.simulator.zones):
            self.assertIsInstance(zone.moisture, (int, float))
            self.assertIsInstance(zone.ph, (int, float))
            self.assertGreaterEqual(zone.moisture, 0)
            self.assertLessEqual(zone.moisture, 100)
            self.assertGreaterEqual(zone.ph, 0)
            self.assertLessEqual(zone.ph, 14)
    
    def test_simulate_with_empty_zones(self):
        """Test simulator with empty zones list"""
        empty_simulator = SensorSimulator([])
        empty_simulator.simulate()
        
        # Should not raise any errors
        self.assertEqual(len(empty_simulator.zones), 0)
    
    def test_simulate_multiple_times(self):
        """Test multiple simulation runs"""
        initial_moisture = self.simulator.zones[0].moisture
        
        # Run simulation multiple times
        for _ in range(5):
            self.simulator.simulate()
        
        # Values should still be within bounds
        final_moisture = self.simulator.zones[0].moisture
        self.assertGreaterEqual(final_moisture, 0)
        self.assertLessEqual(final_moisture, 100)
    
    def test_simulate_realistic_values(self):
        """Test that simulated values are realistic"""
        self.simulator.simulate()
        
        for zone in self.simulator.zones:
            # Moisture should be realistic for gardening
            self.assertGreaterEqual(zone.moisture, 10)  # Not completely dry
            self.assertLessEqual(zone.moisture, 90)     # Not completely saturated
            
            # pH should be realistic for soil
            self.assertGreaterEqual(zone.ph, 5.0)       # Not too acidic
            self.assertLessEqual(zone.ph, 8.5)          # Not too alkaline
    
    @patch('smart_gardening.simulator.simulator.random.uniform')
    def test_simulate_with_mocked_random(self, mock_uniform):
        """Test simulation with mocked random values"""
        # Mock random values
        mock_uniform.side_effect = [50.0, 6.5, 60.0, 7.0, 40.0, 6.8]
        
        self.simulator.simulate()
        
        # Check that random.uniform was called
        self.assertTrue(mock_uniform.called)
        
        # Check that zones were updated with mocked values
        self.assertEqual(self.simulator.zones[0].moisture, 50.0)
        self.assertEqual(self.simulator.zones[0].ph, 6.5)
        self.assertEqual(self.simulator.zones[1].moisture, 60.0)
        self.assertEqual(self.simulator.zones[1].ph, 7.0)
        self.assertEqual(self.simulator.zones[2].moisture, 40.0)
        self.assertEqual(self.simulator.zones[2].ph, 6.8)
    
    def test_simulator_with_different_zone_types(self):
        """Test simulator with different types of zones"""
        diverse_zones = [
            Zone(id=1, name="Dry Zone", plant_type="Cactus", moisture=20, ph=7.5),
            Zone(id=2, name="Wet Zone", plant_type="Rice", moisture=80, ph=6.0),
            Zone(id=3, name="Balanced Zone", plant_type="Tomatoes", moisture=50, ph=6.8)
        ]
        
        diverse_simulator = SensorSimulator(diverse_zones)
        diverse_simulator.simulate()
        
        # All zones should still have valid values
        for zone in diverse_simulator.zones:
            self.assertGreaterEqual(zone.moisture, 0)
            self.assertLessEqual(zone.moisture, 100)
            self.assertGreaterEqual(zone.ph, 0)
            self.assertLessEqual(zone.ph, 14)


if __name__ == '__main__':
    unittest.main() 