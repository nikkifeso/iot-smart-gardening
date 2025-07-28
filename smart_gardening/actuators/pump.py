from datetime import datetime

def activate_pump(zone_id: str):
    print(f"[PUMP] Zone {zone_id}: Water pump activated")

def deactivate_pump(zone_id: str):
    print(f"[PUMP] Zone {zone_id}: Water pump deactivated")

def control_pump(zone_id: str, status: bool):
    if status:
        activate_pump(zone_id)
    else:
        deactivate_pump(zone_id)


class WaterPump:
    """Water pump controller for a specific zone"""
    
    def __init__(self, zone_id: int):
        self.zone_id = zone_id
        self.status = "OFF"
        self.last_activated = None
    
    def activate(self):
        """Activate the water pump"""
        self.status = "ON"
        self.last_activated = datetime.now()
        activate_pump(str(self.zone_id))
    
    def deactivate(self):
        """Deactivate the water pump"""
        self.status = "OFF"
        deactivate_pump(str(self.zone_id))
    
    def toggle(self):
        """Toggle the pump status"""
        if self.status == "OFF":
            self.activate()
        else:
            self.deactivate()
    
    def __str__(self):
        return f"WaterPump(Zone {self.zone_id}, Status: {self.status})"