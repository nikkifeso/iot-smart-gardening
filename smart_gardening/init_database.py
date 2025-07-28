#!/usr/bin/env python3
"""
Database initialization script for Smart Gardening System
Creates tables with auto-incrementing IDs for zones
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database import init_db, session, ZoneModel, PlantModel
from core.zone import Zone

def init_database():
    """Initialize the database with new schema"""
    print("Initializing database with new schema...")
    
    # Create all tables
    init_db()
    
    # Create some default zones
    default_zones = [
        {
            'name': 'Tomato Garden',
            'plant_type': 'Tomato',
            'moisture_threshold': 40,
            'ph_min': 6.0,
            'ph_max': 6.8
        },
        {
            'name': 'Lettuce Patch',
            'plant_type': 'Lettuce',
            'moisture_threshold': 45,
            'ph_min': 6.2,
            'ph_max': 7.0
        },
        {
            'name': 'Herb Garden',
            'plant_type': 'Herbs',
            'moisture_threshold': 50,
            'ph_min': 5.5,
            'ph_max': 7.2
        }
    ]
    
    created_zones = []
    for zone_data in default_zones:
        db_zone = ZoneModel(**zone_data)
        session.add(db_zone)
        session.commit()
        created_zones.append(db_zone)
        print(f"Created zone: {db_zone.name} with ID: {db_zone.id}")
    
    # Add some sample plants
    sample_plants = [
        {'zone_id': 1, 'name': 'Cherry Tomato', 'plant_type': 'Tomato', 'notes': 'Sweet cherry variety'},
        {'zone_id': 2, 'name': 'Butterhead Lettuce', 'plant_type': 'Lettuce', 'notes': 'Tender butterhead variety'},
        {'zone_id': 3, 'name': 'Basil', 'plant_type': 'Herbs', 'notes': 'Sweet basil for cooking'},
    ]
    
    for plant_data in sample_plants:
        db_plant = PlantModel(**plant_data)
        session.add(db_plant)
        session.commit()
        print(f"Added plant: {db_plant.name} to zone {db_plant.zone_id}")
    
    print("Database initialization completed successfully!")
    return created_zones

if __name__ == "__main__":
    init_database() 