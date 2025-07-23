import random

class SensorSimulator:
    def __init__(self, zones) -> None:
        """
        :param zones: List of zone Objects
        """
        self.zones = zones

    def simulate(self):
        """
        Simulate sensor reading for all zones and update the Zone objects.
        """
        for zone in self.zones:
            # simulate moisture %
            moisture = random.uniform(10,80)

            # simulate pH value
            ph = random.uniform(4.5, 8.5)

            zone.update_readings(moisture, ph)
