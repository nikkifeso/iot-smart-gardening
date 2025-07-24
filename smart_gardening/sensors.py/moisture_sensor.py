import random

def read_moisture(zone_id: str) -> float:
    # Define zone-specific moisture ranges
    zone_moisture_ranges = {
        "zone_1": (20, 40),
        "zone_2": (40, 60),
        "zone_3": (60, 80),
    }
    
    # Get the moisture range for the specified zone
    if zone_id in zone_moisture_ranges:
        min_moisture, max_moisture = zone_moisture_ranges[zone_id]
        return round(random.uniform(min_moisture, max_moisture), 2)
    else:
        raise ValueError(f"Invalid zone_id: {zone_id}")
