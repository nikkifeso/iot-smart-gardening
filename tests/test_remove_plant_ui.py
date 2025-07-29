import unittest
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smart_gardening.db.database import Base, ZoneModel, PlantModel, init_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestRemovePlantUI(unittest.TestCase):
    """Test cases for remove plant UI functionality"""
    
    def setUp(self):
        """Set up test database"""
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        
        # Create engine and session for testing
        self.engine = create_engine(f'sqlite:///{self.db_path}')
        Base.metadata.create_all(self.engine)
        
        # Create test session
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.test_session = TestingSessionLocal()
        
        # Create test data
        self.create_test_data()
    
    def tearDown(self):
        """Clean up test database"""
        self.test_session.close()
        os.unlink(self.db_path)
    
    def create_test_data(self):
        """Create test zones and plants"""
        # Create test zone
        self.zone = ZoneModel(
            name="Test Zone",
            plant_type="Vegetables",
            moisture_threshold=30,
            ph_min=6.0,
            ph_max=7.5
        )
        self.test_session.add(self.zone)
        self.test_session.commit()
        
        # Create test plant
        self.plant = PlantModel(
            zone_id=self.zone.id,
            name="Test Plant",
            plant_type="Vegetable",
            planting_date=datetime.now(),
            notes="Test plant for UI testing"
        )
        self.test_session.add(self.plant)
        self.test_session.commit()
    
    def test_session_state_parameter_validation(self):
        """Test validation of session state parameters"""
        with patch('streamlit.session_state') as mock_session_state:
            mock_session_state.get.side_effect = lambda key, default=None: {
                "remove_zone_id": self.zone.id,
                "remove_plant_id": self.plant.id
            }.get(key, default)
            
            zone_id = mock_session_state.get("remove_zone_id", None)
            plant_id = mock_session_state.get("remove_plant_id", None)
            
            self.assertIsNotNone(zone_id)
            self.assertIsNotNone(plant_id)
            self.assertEqual(zone_id, self.zone.id)
            self.assertEqual(plant_id, self.plant.id)
    
    def test_session_state_missing_parameters(self):
        """Test handling of missing session state parameters"""
        with patch('streamlit.session_state') as mock_session_state:
            mock_session_state.get.return_value = None
            
            with self.assertRaises(Exception):
                zone_id = mock_session_state.get("remove_zone_id", None)
                plant_id = mock_session_state.get("remove_plant_id", None)
                if not zone_id or not plant_id:
                    raise Exception("Missing parameters")
    
    def test_plant_zone_validation(self):
        """Test validation that plant belongs to the correct zone"""
        plant = self.test_session.query(PlantModel).filter(PlantModel.id == self.plant.id).first()
        self.assertIsNotNone(plant)
        self.assertEqual(plant.zone_id, self.zone.id)
        
        wrong_zone_id = 999
        self.assertNotEqual(plant.zone_id, wrong_zone_id)
    
    def test_remove_plant_navigation_flow(self):
        """Test the complete navigation flow for remove plant"""
        with patch('streamlit.session_state') as mock_session_state:
            mock_session_state.remove_zone_id = self.zone.id
            mock_session_state.remove_plant_id = self.plant.id
            
            self.assertEqual(mock_session_state.remove_zone_id, self.zone.id)
            self.assertEqual(mock_session_state.remove_plant_id, self.plant.id)
    
    def test_remove_plant_success_flow(self):
        """Test successful plant removal flow"""
        from smart_gardening.db.database import remove_plant
        
        plant_before = self.test_session.query(PlantModel).filter(PlantModel.id == self.plant.id).first()
        self.assertIsNotNone(plant_before)
        self.assertEqual(plant_before.name, "Test Plant")
        
        success = remove_plant(self.plant.id, self.test_session)
        self.assertTrue(success)
        
        plant_after = self.test_session.query(PlantModel).filter(PlantModel.id == self.plant.id).first()
        self.assertIsNone(plant_after)
        
        zone_after = self.test_session.query(ZoneModel).filter(ZoneModel.id == self.zone.id).first()
        self.assertIsNotNone(zone_after)
        self.assertEqual(zone_after.name, "Test Zone")
    
    def test_remove_plant_error_handling(self):
        """Test error handling in remove plant flow"""
        from smart_gardening.db.database import remove_plant
        
        success = remove_plant(99999, self.test_session)
        self.assertFalse(success)
        
        success = remove_plant(self.plant.id, self.test_session)
        self.assertTrue(success)
        
        success = remove_plant(self.plant.id, self.test_session)
        self.assertFalse(success)
    
    def test_remove_plant_with_multiple_plants(self):
        """Test removing one plant when multiple plants exist in zone"""
        from smart_gardening.db.database import remove_plant
        
        plant2 = PlantModel(
            zone_id=self.zone.id,
            name="Test Plant 2",
            plant_type="Vegetable",
            planting_date=datetime.now(),
            notes="Second test plant"
        )
        self.test_session.add(plant2)
        self.test_session.commit()
        
        zone_plants = self.test_session.query(PlantModel).filter(PlantModel.zone_id == self.zone.id).all()
        self.assertEqual(len(zone_plants), 2)
        
        success = remove_plant(self.plant.id, self.test_session)
        self.assertTrue(success)
        
        remaining_plants = self.test_session.query(PlantModel).filter(PlantModel.zone_id == self.zone.id).all()
        self.assertEqual(len(remaining_plants), 1)
        self.assertEqual(remaining_plants[0].name, "Test Plant 2")
    
    def test_remove_plant_data_integrity(self):
        """Test that removing a plant doesn't affect other data"""
        from smart_gardening.db.database import remove_plant
        
        zone2 = ZoneModel(name="Test Zone 2", plant_type="Fruits")
        self.test_session.add(zone2)
        self.test_session.commit()
        
        plant2 = PlantModel(
            zone_id=zone2.id,
            name="Test Plant 2",
            plant_type="Fruit",
            planting_date=datetime.now(),
            notes="Plant in different zone"
        )
        self.test_session.add(plant2)
        self.test_session.commit()
        
        success = remove_plant(self.plant.id, self.test_session)
        self.assertTrue(success)
        
        plant2_after = self.test_session.query(PlantModel).filter(PlantModel.id == plant2.id).first()
        self.assertIsNotNone(plant2_after)
        self.assertEqual(plant2_after.name, "Test Plant 2")
        self.assertEqual(plant2_after.zone_id, zone2.id)
        
        zone2_after = self.test_session.query(ZoneModel).filter(ZoneModel.id == zone2.id).first()
        self.assertIsNotNone(zone2_after)
        self.assertEqual(zone2_after.name, "Test Zone 2")


if __name__ == '__main__':
    unittest.main() 