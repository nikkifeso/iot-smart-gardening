def activate_pump(zone_id: str):
    print(f"[PUMP] Zone {zone_id}: Water pump activated")

def deactivate_pump(zone_id: str):
    print(f"[PUMP] Zone {zone_id}: Water pump deactivated")

def control_pump(zone_id: str, status: bool):
    if status:
        activate_pump(zone_id)
    else:
        deactivate_pump(zone_id)