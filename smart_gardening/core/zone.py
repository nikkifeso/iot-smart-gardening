class Zone:
    def __init__(self, id, name, plant_type, moisture_threshold, moisture, ph_range, ph):
        self.id = id
        self.name = name
        self.plant_type = [plant_type]
        self.moisture_threshold = moisture_threshold
        # (min, max) tuple
        self.ph_range = ph_range  
        self.moisture = moisture
        self.ph = ph
        self.pump_status = False

    def update_readings(self, moisture, ph):
        self.moisture = moisture
        self.ph = ph

    def needs_watering(self):
        return self.moisture is not None and self.moisture < self.moisture_threshold

    def ph_out_of_range(self):
        if self.ph is None:
            return False
        return not (self.ph_range[0] <= self.ph <= self.ph_range[1])
