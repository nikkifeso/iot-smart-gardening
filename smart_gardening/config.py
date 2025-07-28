# config.py
import os

ZONES = ["A", "B", "C"]

MOISTURE_THRESHOLDS = {
    "A": 40,  # Zone A: minimum acceptable moisture level
    "B": 45,  # Zone B: minimum acceptable moisture level
    "C": 50,  # Zone C: minimum acceptable moisture level
}

# Optional: pH ranges or other parameters
PH_RANGES = {
    "A": (6.0, 6.8),
    "B": (6.2, 7.0),
    "C": (5.5, 7.2),
}

SCHEDULE = {
    "hour": 6,  # Simulated schedule time for daily watering check
}


class Config:
    """Configuration management for the Smart Gardening Dashboard"""
    
    def __init__(self):
        # Database configuration
        db_url = os.getenv('DATABASE_URL', 'sqlite:///smart_garden.db')
        self.DATABASE_URL = db_url if db_url else 'sqlite:///smart_garden.db'
        
        # Sensor configuration
        try:
            interval = int(os.getenv('SENSOR_READING_INTERVAL', '300'))
            self.SENSOR_READING_INTERVAL = interval if interval > 0 else 300
        except (ValueError, TypeError):
            self.SENSOR_READING_INTERVAL = 300
        
        # Pump configuration
        try:
            duration = int(os.getenv('PUMP_ACTIVATION_DURATION', '30'))
            self.PUMP_ACTIVATION_DURATION = duration if duration > 0 else 30
        except (ValueError, TypeError):
            self.PUMP_ACTIVATION_DURATION = 30
        
        # Default thresholds
        try:
            threshold = int(os.getenv('DEFAULT_MOISTURE_THRESHOLD', '30'))
            self.DEFAULT_MOISTURE_THRESHOLD = threshold if threshold >= 0 else 30
        except (ValueError, TypeError):
            self.DEFAULT_MOISTURE_THRESHOLD = 30
        
        try:
            ph_min = float(os.getenv('DEFAULT_PH_MIN', '6.0'))
            self.DEFAULT_PH_MIN = ph_min if 0 <= ph_min <= 14 else 6.0
        except (ValueError, TypeError):
            self.DEFAULT_PH_MIN = 6.0
        
        try:
            ph_max = float(os.getenv('DEFAULT_PH_MAX', '7.5'))
            self.DEFAULT_PH_MAX = ph_max if 0 <= ph_max <= 14 else 7.5
        except (ValueError, TypeError):
            self.DEFAULT_PH_MAX = 7.5
    
    def to_dict(self):
        """Convert configuration to dictionary"""
        return {
            'DATABASE_URL': self.DATABASE_URL,
            'SENSOR_READING_INTERVAL': self.SENSOR_READING_INTERVAL,
            'PUMP_ACTIVATION_DURATION': self.PUMP_ACTIVATION_DURATION,
            'DEFAULT_MOISTURE_THRESHOLD': self.DEFAULT_MOISTURE_THRESHOLD,
            'DEFAULT_PH_MIN': self.DEFAULT_PH_MIN,
            'DEFAULT_PH_MAX': self.DEFAULT_PH_MAX
        }
    
    def __str__(self):
        return f"Config(DATABASE_URL={self.DATABASE_URL}, SENSOR_READING_INTERVAL={self.SENSOR_READING_INTERVAL}s)"
