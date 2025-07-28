import unittest
import sys
import os
import tempfile
from unittest.mock import patch, MagicMock

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smart_gardening.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for configuration management"""
    
    def setUp(self):
        """Set up test environment"""
        self.config = Config()
    
    def test_default_configuration(self):
        """Test default configuration values"""
        # Test database configuration
        self.assertIsInstance(self.config.DATABASE_URL, str)
        self.assertIn("sqlite", self.config.DATABASE_URL.lower())
        
        # Test sensor configuration
        self.assertIsInstance(self.config.SENSOR_READING_INTERVAL, int)
        self.assertGreater(self.config.SENSOR_READING_INTERVAL, 0)
        
        # Test pump configuration
        self.assertIsInstance(self.config.PUMP_ACTIVATION_DURATION, int)
        self.assertGreater(self.config.PUMP_ACTIVATION_DURATION, 0)
        
        # Test threshold configuration
        self.assertIsInstance(self.config.DEFAULT_MOISTURE_THRESHOLD, int)
        self.assertGreaterEqual(self.config.DEFAULT_MOISTURE_THRESHOLD, 0)
        self.assertLessEqual(self.config.DEFAULT_MOISTURE_THRESHOLD, 100)
        
        self.assertIsInstance(self.config.DEFAULT_PH_MIN, float)
        self.assertGreaterEqual(self.config.DEFAULT_PH_MIN, 0)
        self.assertLessEqual(self.config.DEFAULT_PH_MIN, 14)
        
        self.assertIsInstance(self.config.DEFAULT_PH_MAX, float)
        self.assertGreaterEqual(self.config.DEFAULT_PH_MAX, 0)
        self.assertLessEqual(self.config.DEFAULT_PH_MAX, 14)
        
        # Verify pH range is valid
        self.assertLess(self.config.DEFAULT_PH_MIN, self.config.DEFAULT_PH_MAX)
    
    def test_environment_variable_override(self):
        """Test configuration override with environment variables"""
        # Test with custom database URL
        with patch.dict(os.environ, {'DATABASE_URL': 'sqlite:///test.db'}):
            config = Config()
            self.assertEqual(config.DATABASE_URL, 'sqlite:///test.db')
        
        # Test with custom sensor interval
        with patch.dict(os.environ, {'SENSOR_READING_INTERVAL': '300'}):
            config = Config()
            self.assertEqual(config.SENSOR_READING_INTERVAL, 300)
        
        # Test with custom pump duration
        with patch.dict(os.environ, {'PUMP_ACTIVATION_DURATION': '60'}):
            config = Config()
            self.assertEqual(config.PUMP_ACTIVATION_DURATION, 60)
        
        # Test with custom moisture threshold
        with patch.dict(os.environ, {'DEFAULT_MOISTURE_THRESHOLD': '25'}):
            config = Config()
            self.assertEqual(config.DEFAULT_MOISTURE_THRESHOLD, 25)
        
        # Test with custom pH range
        with patch.dict(os.environ, {'DEFAULT_PH_MIN': '5.5', 'DEFAULT_PH_MAX': '7.0'}):
            config = Config()
            self.assertEqual(config.DEFAULT_PH_MIN, 5.5)
            self.assertEqual(config.DEFAULT_PH_MAX, 7.0)
    
    def test_invalid_environment_variables(self):
        """Test handling of invalid environment variables"""
        # Test invalid integer values
        with patch.dict(os.environ, {'SENSOR_READING_INTERVAL': 'invalid'}):
            config = Config()
            # Should fall back to default value
            self.assertIsInstance(config.SENSOR_READING_INTERVAL, int)
        
        # Test invalid float values
        with patch.dict(os.environ, {'DEFAULT_PH_MIN': 'invalid'}):
            config = Config()
            # Should fall back to default value
            self.assertIsInstance(config.DEFAULT_PH_MIN, float)
        
        # Test negative values
        with patch.dict(os.environ, {'SENSOR_READING_INTERVAL': '-10'}):
            config = Config()
            # Should fall back to default value
            self.assertGreater(config.SENSOR_READING_INTERVAL, 0)
    
    def test_configuration_validation(self):
        """Test configuration value validation"""
        # Test moisture threshold validation
        self.assertGreaterEqual(self.config.DEFAULT_MOISTURE_THRESHOLD, 0)
        self.assertLessEqual(self.config.DEFAULT_MOISTURE_THRESHOLD, 100)
        
        # Test pH range validation
        self.assertGreaterEqual(self.config.DEFAULT_PH_MIN, 0)
        self.assertLessEqual(self.config.DEFAULT_PH_MIN, 14)
        self.assertGreaterEqual(self.config.DEFAULT_PH_MAX, 0)
        self.assertLessEqual(self.config.DEFAULT_PH_MAX, 14)
        self.assertLess(self.config.DEFAULT_PH_MIN, self.config.DEFAULT_PH_MAX)
        
        # Test timing validation
        self.assertGreater(self.config.SENSOR_READING_INTERVAL, 0)
        self.assertGreater(self.config.PUMP_ACTIVATION_DURATION, 0)
    
    def test_configuration_persistence(self):
        """Test that configuration values persist across instances"""
        # Create first config instance
        config1 = Config()
        original_db_url = config1.DATABASE_URL
        original_interval = config1.SENSOR_READING_INTERVAL
        
        # Create second config instance
        config2 = Config()
        
        # Values should be the same
        self.assertEqual(config1.DATABASE_URL, config2.DATABASE_URL)
        self.assertEqual(config1.SENSOR_READING_INTERVAL, config2.SENSOR_READING_INTERVAL)
        self.assertEqual(config1.PUMP_ACTIVATION_DURATION, config2.PUMP_ACTIVATION_DURATION)
        self.assertEqual(config1.DEFAULT_MOISTURE_THRESHOLD, config2.DEFAULT_MOISTURE_THRESHOLD)
        self.assertEqual(config1.DEFAULT_PH_MIN, config2.DEFAULT_PH_MIN)
        self.assertEqual(config1.DEFAULT_PH_MAX, config2.DEFAULT_PH_MAX)
    
    def test_configuration_methods(self):
        """Test configuration utility methods"""
        # Test getting configuration as dictionary
        config_dict = self.config.to_dict()
        
        self.assertIsInstance(config_dict, dict)
        self.assertIn('DATABASE_URL', config_dict)
        self.assertIn('SENSOR_READING_INTERVAL', config_dict)
        self.assertIn('PUMP_ACTIVATION_DURATION', config_dict)
        self.assertIn('DEFAULT_MOISTURE_THRESHOLD', config_dict)
        self.assertIn('DEFAULT_PH_MIN', config_dict)
        self.assertIn('DEFAULT_PH_MAX', config_dict)
        
        # Test configuration string representation
        config_str = str(self.config)
        self.assertIsInstance(config_str, str)
        self.assertIn('DATABASE_URL', config_str)
        self.assertIn('SENSOR_READING_INTERVAL', config_str)
    
    def test_configuration_for_different_environments(self):
        """Test configuration for different deployment environments"""
        # Test development environment
        with patch.dict(os.environ, {'ENVIRONMENT': 'development'}):
            config = Config()
            # Development should use local database
            self.assertIn('sqlite', config.DATABASE_URL.lower())
        
        # Test production environment
        with patch.dict(os.environ, {'ENVIRONMENT': 'production', 'DATABASE_URL': 'postgresql://prod.db'}):
            config = Config()
            # Production should use provided database URL
            self.assertEqual(config.DATABASE_URL, 'postgresql://prod.db')
        
        # Test testing environment
        with patch.dict(os.environ, {'ENVIRONMENT': 'testing', 'DATABASE_URL': 'sqlite:///test.db'}):
            config = Config()
            # Testing should use test database
            self.assertEqual(config.DATABASE_URL, 'sqlite:///test.db')
    
    def test_configuration_edge_cases(self):
        """Test configuration edge cases"""
        # Test with empty environment variables
        with patch.dict(os.environ, {'DATABASE_URL': ''}):
            config = Config()
            # Should fall back to default
            self.assertIsInstance(config.DATABASE_URL, str)
            self.assertGreater(len(config.DATABASE_URL), 0)
        
        # Test with very large values
        with patch.dict(os.environ, {'SENSOR_READING_INTERVAL': '999999'}):
            config = Config()
            # Should accept large values
            self.assertEqual(config.SENSOR_READING_INTERVAL, 999999)
        
        # Test with zero values
        with patch.dict(os.environ, {'SENSOR_READING_INTERVAL': '0'}):
            config = Config()
            # Should fall back to default (positive value)
            self.assertGreater(config.SENSOR_READING_INTERVAL, 0)
    
    def test_configuration_type_consistency(self):
        """Test that configuration types are consistent"""
        # All timing values should be integers
        self.assertIsInstance(self.config.SENSOR_READING_INTERVAL, int)
        self.assertIsInstance(self.config.PUMP_ACTIVATION_DURATION, int)
        
        # Threshold values should be appropriate types
        self.assertIsInstance(self.config.DEFAULT_MOISTURE_THRESHOLD, int)
        self.assertIsInstance(self.config.DEFAULT_PH_MIN, float)
        self.assertIsInstance(self.config.DEFAULT_PH_MAX, float)
        
        # Database URL should be string
        self.assertIsInstance(self.config.DATABASE_URL, str)


if __name__ == '__main__':
    unittest.main() 