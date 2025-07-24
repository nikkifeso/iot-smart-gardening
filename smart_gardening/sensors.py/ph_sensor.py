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
