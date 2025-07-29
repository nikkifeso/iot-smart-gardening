import random

def read_ph(zone_id: str) -> float:
    """
    Read pH level for any zone.
    
    Args:
        zone_id: Zone identifier (e.g., 'zone_1', 'zone_5', 'garden_a')
    
    Returns:
        float: pH reading between 5.0-8.5
    """
    return round(random.uniform(5.0, 8.5), 2)


class PHSensor:
    """pH sensor for a specific zone"""
    
    def __init__(self, zone_id: int):
        self.zone_id = zone_id
        self.current_reading = self.read()
    
    def read(self) -> float:
        """Read current pH level"""
        reading = round(random.uniform(5.0, 8.5), 2)
        self.current_reading = reading
        return reading
    
    def __str__(self):
        return f"PHSensor(Zone {self.zone_id}, pH: {self.current_reading})"
