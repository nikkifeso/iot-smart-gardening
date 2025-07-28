import random

def read_moisture(zone_id: str) -> float:
    """
    Read moisture level for any zone.
    
    Args:
        zone_id: Zone identifier (e.g., 'zone_1', 'zone_5', 'garden_a')
    
    Returns:
        float: Moisture reading between 10-90%
    """
    # Generate realistic moisture reading (10-90% range) for any zone
    # This matches the behavior of the MoistureSensor class
    return round(random.uniform(10, 90), 2)


class MoistureSensor:
    """Moisture sensor for a specific zone"""
    
    def __init__(self, zone_id: int):
        self.zone_id = zone_id
        self.current_reading = self.read()
    
    def read(self) -> float:
        """Read current moisture level"""
        # Generate realistic moisture reading (10-90% range)
        reading = round(random.uniform(10, 90), 2)
        self.current_reading = reading
        return reading
    
    def __str__(self):
        return f"MoistureSensor(Zone {self.zone_id}, Reading: {self.current_reading}%)"
