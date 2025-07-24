# config.py

ZONES = ["A", "B", "C"]

MOISTURE_THRESHOLDS = {
    "A": 40,  # Zone A: minimum acceptable moisture level
    "B": 45,  # Zone B: minimum acceptable moisture level
    "C": 50,  # Zone C: minimum acceptable moisture level
}

# Optional: pH ranges or other parameters
PH_RANGES = {
    "A": (6.0, 6.8),
    "B": (6.2, 7.0),
    "C": (5.5, 7.2),
}

SCHEDULE = {
    "hour": 6,  # Simulated schedule time for daily watering check
}
