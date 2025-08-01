import time
from datetime import datetime, timedelta
from smart_gardening.simulator.simulator import SensorSimulator, get_default_zones
from smart_gardening.actuators.pump import  control_pump
from smart_gardening.db.database import session, SensorReading, init_db, cleanup_old_sensor_readings


if __name__ == "__main__":
    init_db()
    print("Starting Smart Irrigation System Simulation...")
    print("Sensor readings will be updated every 30 seconds...")
    print("Data retention: 60 days (automatic cleanup)")

    zones = get_default_zones()
    simulator = SensorSimulator(zones)
    
    # Track when last cleanup was performed
    last_cleanup = datetime.now()
    cleanup_interval = timedelta(days=1)  # Run cleanup once per day
    
    try:
        while True:
            print(f"\n--- Sensor Reading Update at {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
            
            # Simulate new sensor readings
            simulator.simulate()

            for zone in zones:
                # Create new sensor reading record
                reading = SensorReading(
                    zone_id=zone.id,
                    moisture=zone.moisture,
                    ph=zone.ph
                )
                session.add(reading)
                
                # Advanced automation logic
                if zone.pump_status:  # Pump is currently running
                    if zone.should_deactivate_pump():
                        # Stop pump if moisture is sufficient or max runtime reached
                        control_pump(zone.id, False)
                        zone.stop_pump()
                        reason = "moisture sufficient" if zone.moisture >= zone.moisture_threshold else "max runtime reached"
                        print(f"Zone {zone.name}: Pump stopped - {reason}")
                    else:
                        # Pump continues running
                        print(f"Zone {zone.name}: Pump running - Moisture={zone.moisture}%, pH={zone.ph}")
                else:  # Pump is currently off
                    if zone.should_activate_pump():
                        # Start pump if needed and allowed
                        control_pump(zone.id, True)
                        zone.start_pump()
                        print(f"Zone {zone.name}: Pump started - Moisture={zone.moisture}%, pH={zone.ph}")
                    else:
                        # Pump remains off
                        reason = "moisture sufficient" if zone.moisture >= zone.moisture_threshold else "recent watering"
                        print(f"Zone {zone.name}: Pump off - {reason} (Moisture={zone.moisture}%, pH={zone.ph})")

                status_str = "ON" if zone.pump_status else "OFF"
                print(f"Zone {zone.name}: Final Status - Moisture={zone.moisture}%, pH={zone.ph}, Pump={status_str}")
            
            session.commit()
            
            # Check if it's time for data cleanup (once per day)
            current_time = datetime.now()
            if current_time - last_cleanup >= cleanup_interval:
                print(f"\n🧹 Running scheduled data cleanup at {current_time.strftime('%Y-%m-%d %H:%M:%S')}...")
                deleted_count = cleanup_old_sensor_readings(retention_days=60)
                if deleted_count > 0:
                    print(f"✅ Cleaned up {deleted_count} old records")
                else:
                    print("✅ No old records to clean up")
                last_cleanup = current_time
                print("Waiting 30 seconds until next update...")
            else:
                print("Waiting 30 seconds until next update...")
            
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
        session.close()
