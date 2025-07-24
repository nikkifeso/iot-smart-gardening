from simulator.simulator import SensorSimulator, get_default_zones
from actuators.pump import activate_pump, deactivate_pump

if __name__ == "__main__":
    print("Starting Smart Irrigation System Simulation...")

    zones = get_default_zones()
    simulator = SensorSimulator(zones)
    simulator.simulate()

    for zone in zones:
        print(f"[{zone.name}] Moisture: {zone.moisture}%, pH: {zone.ph}")
        if zone.moisture < zone.moisture_threshold:
            activate_pump(zone.id)
            zone.pump_status = True
        else:
            deactivate_pump(zone.id)
            zone.pump_status = False
