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

    def update_readings(self, moisture, ph):
        self.moisture = moisture
        self.ph = ph

    def needs_watering(self):
        return self.moisture is not None and self.moisture < self.moisture_threshold

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
