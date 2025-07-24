import random
from core.zone import Zone

class SensorSimulator:
    def __init__(self, zones) -> None:
        """
        :param zones: List of zone Objects
        """
        self.zones = zones

    def simulate(self):
        for zone in self.zones:
            zone.moisture = round(random.uniform(20, 80), 2)
            zone.ph = round(random.uniform(5.5, 7.5), 2)

    def get_data(self):
        return [
            {
                "zone": zone.name,
                "moisture": zone.moisture,
                "ph": zone.ph,
                "pump_status": zone.pump_status
            }
            for zone in self.zones
        ]

def get_default_zones():
    return [
        Zone(id="A", name="Zone A", moisture_threshold=40, ph_range=(6.0, 7.0), plant_type=["Cactus", "Spider Lily"], moisture=5, ph=7, pump_status=False),
        Zone(id="B", name="Zone B", moisture_threshold=45, ph_range=(6.2, 7.2), plant_type=["Tomato"], moisture=5, ph=9, pump_status=False),
        Zone(id="C", name="Zone C", moisture_threshold=50, ph_range=(5.8, 6.8), plant_type=["Sunflower"], moisture=5, ph=4, pump_status=False),
    ]
