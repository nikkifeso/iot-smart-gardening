import random

def read_ph(zone_id: str) -> float:
    # Define pH ranges for specific zones
    zone_ph_ranges = {
        "zone_1": (5.5, 6.5),
        "zone_2": (6.0, 7.0),
        "zone_3": (6.5, 7.5),
    }
    
    # Get the pH range for the given zone_id
    if zone_id in zone_ph_ranges:
        min_ph, max_ph = zone_ph_ranges[zone_id]
        return round(random.uniform(min_ph, max_ph), 2)
    else:
        raise ValueError(f"Invalid zone_id: {zone_id}")


class PHSensor:
    """pH sensor for a specific zone"""
    
    def __init__(self, zone_id: int):
        self.zone_id = zone_id
        self.current_reading = self.read()
    
    def read(self) -> float:
        """Read current pH level"""
        # Generate realistic pH reading (5.0-8.5 range for soil)
        reading = round(random.uniform(5.0, 8.5), 2)
        self.current_reading = reading
        return reading
    
    def __str__(self):
        return f"PHSensor(Zone {self.zone_id}, pH: {self.current_reading})"
