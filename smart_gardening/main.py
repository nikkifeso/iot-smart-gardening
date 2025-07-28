from simulator.simulator import SensorSimulator, get_default_zones
from actuators.pump import  control_pump
from db.database import session, SensorReading, init_db


if __name__ == "__main__":
    init_db()
    print("Starting Smart Irrigation System Simulation...")

    zones = get_default_zones()
    simulator = SensorSimulator(zones)
    simulator.simulate()

    for zone in zones:
        reading = SensorReading(
            zone_id=zone.id,
            moisture=zone.moisture,
            ph=zone.ph
        )
        session.add(reading)
        if zone.moisture < zone.moisture_threshold:
            control_pump(zone.id, True)
            zone.pump_status = True
        else:
            control_pump(zone.id, False)
            zone.pump_status = False

        status_str = "ON" if zone.pump_status else "OFF"
        print(f"Pump status: {status_str}")
    session.commit()
