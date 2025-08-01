from datetime import datetime, timedelta

class Zone:
    def __init__(self, id=None, name=None, plant_type=None, moisture_threshold=30, moisture=50, ph_range=(6.0, 7.5), ph=6.5, pump_status="OFF"):
        self.id = id
        self.name = name
        self.plant_type = plant_type
        self.moisture_threshold = moisture_threshold
        self.ph_range = ph_range  
        self.moisture = moisture
        self.ph = ph
        self.pump_status = pump_status
        self.plants = []
        self.last_watering_time = None
        self.pump_start_time = None
        self.max_runtime_minutes = 30  #in minutes

    def update_readings(self, moisture, ph):
        self.moisture = moisture
        self.ph = ph

    def needs_watering(self):
        """Check if zone needs watering based on moisture threshold"""
        return self.moisture is not None and self.moisture < self.moisture_threshold
    
    def can_water(self):
        """Check if zone can be watered (no recent watering > 2 hours)"""
        if self.last_watering_time is None:
            return True
        time_since_last_watering = datetime.now() - self.last_watering_time
        return time_since_last_watering > timedelta(hours=2)
    
    def should_activate_pump(self):
        """Check if pump should be activated"""
        return self.needs_watering() and self.can_water()
    
    def should_deactivate_pump(self):
        """Check if pump should be deactivated"""
        moisture_sufficient = self.moisture >= self.moisture_threshold
        max_runtime_reached = self.is_max_runtime_reached()
        return moisture_sufficient or max_runtime_reached
    
    def is_max_runtime_reached(self):
        """Check if pump has been running for maximum allowed time"""
        if self.pump_start_time is None:
            return False
        runtime = datetime.now() - self.pump_start_time
        return runtime > timedelta(minutes=self.max_runtime_minutes)
    
    def start_pump(self):
        """Start the pump and record start time"""
        self.pump_status = True
        self.pump_start_time = datetime.now()
    
    def stop_pump(self):
        """Stop the pump and record watering time"""
        self.pump_status = False
        self.last_watering_time = datetime.now()
        self.pump_start_time = None

    def ph_out_of_range(self):
        if self.ph is None:
            return False
        return not (self.ph_range[0] <= self.ph <= self.ph_range[1])

    def to_dict(self):
        """Convert zone to dictionary for database operations"""
        return {
            'id': self.id,
            'name': self.name,
            'plant_type': self.plant_type,
            'moisture': self.moisture,
            'ph': self.ph,
            'moisture_threshold': self.moisture_threshold,
            'ph_range': self.ph_range,
            'pump_status': self.pump_status
        }

    @classmethod
    def from_db_model(cls, db_zone):
        """Create Zone instance from database model"""
        zone = cls(
            id=db_zone.id,
            name=db_zone.name,
            plant_type=db_zone.plant_type,
            moisture_threshold=db_zone.moisture_threshold,
            ph_range=(db_zone.ph_min, db_zone.ph_max)
        )
        return zone
    
    def __str__(self):
        """String representation of the zone"""
        return f"Zone(id={self.id}, name='{self.name}', plant_type='{self.plant_type}')"
