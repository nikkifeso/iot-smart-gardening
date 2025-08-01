import unittest
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smart_gardening.core.zone import Zone


class TestAdvancedAutomationLogic(unittest.TestCase):
    
    def setUp(self):
        self.zone = Zone(
            id="A",
            name="Test Zone",
            moisture_threshold=40,
            moisture=35,  # Below threshold
            ph=6.5,
            pump_status=False
        )
    
    def test_needs_watering_logic(self):
        zone_low = Zone(moisture=25, moisture_threshold=40)
        self.assertTrue(zone_low.needs_watering())
        
        zone_at_threshold = Zone(moisture=40, moisture_threshold=40)
        self.assertFalse(zone_at_threshold.needs_watering())
        
        zone_high = Zone(moisture=50, moisture_threshold=40)
        self.assertFalse(zone_high.needs_watering())
        
        zone_none = Zone(moisture=None, moisture_threshold=40)
        self.assertFalse(zone_none.needs_watering())
    
    def test_can_water_logic(self):
        zone_no_history = Zone()
        self.assertTrue(zone_no_history.can_water())
        
        zone_old_watering = Zone()
        zone_old_watering.last_watering_time = datetime.now() - timedelta(hours=3)
        self.assertTrue(zone_old_watering.can_water())
        
        zone_exact_2h = Zone()
        zone_exact_2h.last_watering_time = datetime.now() - timedelta(hours=2)
        self.assertTrue(zone_exact_2h.can_water())
        
        zone_recent_watering = Zone()
        zone_recent_watering.last_watering_time = datetime.now() - timedelta(hours=1)
        self.assertFalse(zone_recent_watering.can_water())
    
    def test_should_activate_pump_logic(self):
        zone_should_activate = Zone(moisture=25, moisture_threshold=40)
        zone_should_activate.last_watering_time = datetime.now() - timedelta(hours=3)
        self.assertTrue(zone_should_activate.should_activate_pump())
        
        zone_recent_watering = Zone(moisture=25, moisture_threshold=40)
        zone_recent_watering.last_watering_time = datetime.now() - timedelta(hours=1)
        self.assertFalse(zone_recent_watering.should_activate_pump())
        
        zone_no_need = Zone(moisture=50, moisture_threshold=40)
        self.assertFalse(zone_no_need.should_activate_pump())
        
        zone_no_need_recent = Zone(moisture=50, moisture_threshold=40)
        zone_no_need_recent.last_watering_time = datetime.now() - timedelta(hours=1)
        self.assertFalse(zone_no_need_recent.should_activate_pump())
    
    def test_should_deactivate_pump_logic(self):
        zone_sufficient_moisture = Zone(moisture=50, moisture_threshold=40)
        zone_sufficient_moisture.pump_status = True
        zone_sufficient_moisture.pump_start_time = datetime.now() - timedelta(minutes=10)
        self.assertTrue(zone_sufficient_moisture.should_deactivate_pump())
        
        zone_max_runtime = Zone(moisture=25, moisture_threshold=40)
        zone_max_runtime.pump_status = True
        zone_max_runtime.pump_start_time = datetime.now() - timedelta(minutes=35)
        self.assertTrue(zone_max_runtime.should_deactivate_pump())
        
        zone_continue_running = Zone(moisture=25, moisture_threshold=40)
        zone_continue_running.pump_status = True
        zone_continue_running.pump_start_time = datetime.now() - timedelta(minutes=15)
        self.assertFalse(zone_continue_running.should_deactivate_pump())
    
    def test_is_max_runtime_reached_logic(self):
        zone_no_start = Zone()
        self.assertFalse(zone_no_start.is_max_runtime_reached())
        
        zone_just_started = Zone()
        zone_just_started.pump_start_time = datetime.now()
        self.assertFalse(zone_just_started.is_max_runtime_reached())
        
        zone_15min = Zone()
        zone_15min.pump_start_time = datetime.now() - timedelta(minutes=15)
        self.assertFalse(zone_15min.is_max_runtime_reached())
        
        zone_30min = Zone()
        zone_30min.pump_start_time = datetime.now() - timedelta(minutes=30)
        self.assertFalse(zone_30min.is_max_runtime_reached())
        
        zone_35min = Zone()
        zone_35min.pump_start_time = datetime.now() - timedelta(minutes=35)
        self.assertTrue(zone_35min.is_max_runtime_reached())
    
    def test_start_pump_method(self):
        zone = Zone(pump_status=False)
        
        self.assertFalse(zone.pump_status)
        self.assertIsNone(zone.pump_start_time)
        
        zone.start_pump()
        
        self.assertTrue(zone.pump_status)
        self.assertIsNotNone(zone.pump_start_time)
        self.assertIsInstance(zone.pump_start_time, datetime)
    
    def test_stop_pump_method(self):
        zone = Zone(pump_status=True)
        zone.pump_start_time = datetime.now() - timedelta(minutes=10)
        
        self.assertTrue(zone.pump_status)
        self.assertIsNotNone(zone.pump_start_time)
        self.assertIsNone(zone.last_watering_time)
        
        zone.stop_pump()
        
        self.assertFalse(zone.pump_status)
        self.assertIsNone(zone.pump_start_time)
        self.assertIsNotNone(zone.last_watering_time)
        self.assertIsInstance(zone.last_watering_time, datetime)
    
    def test_max_runtime_configuration(self):
        zone_default = Zone()
        self.assertEqual(zone_default.max_runtime_minutes, 30)
        
        zone_custom = Zone()
        zone_custom.max_runtime_minutes = 45
        self.assertEqual(zone_custom.max_runtime_minutes, 45)
        
        zone_custom.pump_status = True
        zone_custom.pump_start_time = datetime.now() - timedelta(minutes=40)
        self.assertFalse(zone_custom.is_max_runtime_reached())
        
        zone_custom.pump_start_time = datetime.now() - timedelta(minutes=50)
        self.assertTrue(zone_custom.is_max_runtime_reached())
    
    def test_complete_automation_cycle(self):
        zone = Zone(moisture=25, moisture_threshold=40)
        
        self.assertEqual(zone.pump_status, "OFF")
        self.assertIsNone(zone.last_watering_time)
        self.assertIsNone(zone.pump_start_time)
        
        self.assertTrue(zone.should_activate_pump())
        
        zone.start_pump()
        self.assertEqual(zone.pump_status, True)
        self.assertIsNotNone(zone.pump_start_time)
        
        zone.moisture = 45
        
        self.assertTrue(zone.should_deactivate_pump())
        
        zone.stop_pump()
        self.assertEqual(zone.pump_status, False)
        self.assertIsNone(zone.pump_start_time)
        self.assertIsNotNone(zone.last_watering_time)
        
        zone.moisture = 25
        self.assertFalse(zone.should_activate_pump())
    
    def test_edge_cases(self):
        zone_very_low = Zone(moisture=0, moisture_threshold=40)
        self.assertTrue(zone_very_low.needs_watering())
        
        zone_very_high = Zone(moisture=100, moisture_threshold=40)
        self.assertFalse(zone_very_high.needs_watering())
        
        zone_zero_threshold = Zone(moisture=10, moisture_threshold=0)
        self.assertFalse(zone_zero_threshold.needs_watering())
        
        zone_negative = Zone(moisture=-5, moisture_threshold=40)
        self.assertTrue(zone_negative.needs_watering())
    
    def test_watering_history_persistence(self):
        zone = Zone()
        
        zone.start_pump()
        start_time_1 = zone.pump_start_time
        zone.stop_pump()
        watering_time_1 = zone.last_watering_time
        
        self.assertIsNotNone(watering_time_1)
        self.assertIsNone(zone.pump_start_time)
        
        with patch('smart_gardening.core.zone.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.now() + timedelta(hours=3)
            
            zone.start_pump()
            start_time_2 = zone.pump_start_time
            zone.stop_pump()
            watering_time_2 = zone.last_watering_time
            
            self.assertIsNotNone(watering_time_2)
            self.assertNotEqual(watering_time_1, watering_time_2)


if __name__ == '__main__':
    unittest.main() 