import unittest
import sys
import os
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smart_gardening.db.database import (
    init_db, 
    cleanup_old_sensor_readings, 
    get_sensor_readings_stats,
    SensorReading,
    PumpLog,
    session
)


class TestDataRetention(unittest.TestCase):
    
    def setUp(self):
        init_db()
        session.query(SensorReading).delete()
        session.query(PumpLog).delete()
        session.commit()
    
    def tearDown(self):
        session.query(SensorReading).delete()
        session.query(PumpLog).delete()
        session.commit()
    
    def test_cleanup_old_sensor_readings(self):
        now = datetime.now(timezone.utc)
        
        recent_reading = SensorReading(
            zone_id=1,
            moisture=50.0,
            ph=6.5,
            timestamp=now - timedelta(days=30)
        )
        session.add(recent_reading)
        
        old_reading = SensorReading(
            zone_id=1,
            moisture=45.0,
            ph=6.8,
            timestamp=now - timedelta(days=70)
        )
        session.add(old_reading)
        
        session.commit()
        
        self.assertEqual(session.query(SensorReading).count(), 2)
        
        deleted_count = cleanup_old_sensor_readings(retention_days=60)
        
        self.assertEqual(deleted_count, 1)
        self.assertEqual(session.query(SensorReading).count(), 1)
        
        remaining = session.query(SensorReading).first()
        self.assertEqual(remaining.moisture, 50.0)
    
    def test_cleanup_pump_logs(self):
        now = datetime.now(timezone.utc)
        
        recent_log = PumpLog(
            zone_id=1,
            status="ON",
            timestamp=now - timedelta(days=30)
        )
        session.add(recent_log)
        
        old_log = PumpLog(
            zone_id=1,
            status="OFF",
            timestamp=now - timedelta(days=70)
        )
        session.add(old_log)
        
        session.commit()
        
        self.assertEqual(session.query(PumpLog).count(), 2)
        
        deleted_count = cleanup_old_pump_logs(retention_days=60)
        
        self.assertEqual(deleted_count, 1)
        self.assertEqual(session.query(PumpLog).count(), 1)
        
        remaining = session.query(PumpLog).first()
        self.assertEqual(remaining.status, "ON")
    
    def test_cleanup_mixed_data(self):
        now = datetime.now(timezone.utc)
        
        recent_reading = SensorReading(
            zone_id=1,
            moisture=50.0,
            ph=6.5,
            timestamp=now - timedelta(days=30)
        )
        old_reading = SensorReading(
            zone_id=1,
            moisture=45.0,
            ph=6.8,
            timestamp=now - timedelta(days=70)
        )
        recent_log = PumpLog(
            zone_id=1,
            status="ON",
            timestamp=now - timedelta(days=30)
        )
        old_log = PumpLog(
            zone_id=1,
            status="OFF",
            timestamp=now - timedelta(days=70)
        )
        
        session.add_all([recent_reading, old_reading, recent_log, old_log])
        session.commit()
        
        self.assertEqual(session.query(SensorReading).count(), 2)
        self.assertEqual(session.query(PumpLog).count(), 2)
        
        deleted_count = cleanup_old_sensor_readings(retention_days=60)
        
        self.assertEqual(deleted_count, 2)
        self.assertEqual(session.query(SensorReading).count(), 1)
        self.assertEqual(session.query(PumpLog).count(), 1)
    
    def test_cleanup_no_old_data(self):
        now = datetime.now(timezone.utc)
        
        recent_reading = SensorReading(
            zone_id=1,
            moisture=50.0,
            ph=6.5,
            timestamp=now - timedelta(days=30)
        )
        recent_log = PumpLog(
            zone_id=1,
            status="ON",
            timestamp=now - timedelta(days=30)
        )
        
        session.add_all([recent_reading, recent_log])
        session.commit()
        
        self.assertEqual(session.query(SensorReading).count(), 1)
        self.assertEqual(session.query(PumpLog).count(), 1)
        
        deleted_count = cleanup_old_sensor_readings(retention_days=60)
        
        self.assertEqual(deleted_count, 0)
        self.assertEqual(session.query(SensorReading).count(), 1)
        self.assertEqual(session.query(PumpLog).count(), 1)
    
    def test_cleanup_empty_database(self):
        self.assertEqual(session.query(SensorReading).count(), 0)
        self.assertEqual(session.query(PumpLog).count(), 0)
        
        deleted_count = cleanup_old_sensor_readings(retention_days=60)
        
        self.assertEqual(deleted_count, 0)
        self.assertEqual(session.query(SensorReading).count(), 0)
        self.assertEqual(session.query(PumpLog).count(), 0)
    
    def test_get_sensor_readings_stats(self):
        now = datetime.now(timezone.utc)
        
        reading1 = SensorReading(
            zone_id=1,
            moisture=50.0,
            ph=6.5,
            timestamp=now - timedelta(days=2)
        )
        reading2 = SensorReading(
            zone_id=1,
            moisture=45.0,
            ph=6.8,
            timestamp=now
        )
        
        session.add_all([reading1, reading2])
        session.commit()
        
        stats = get_sensor_readings_stats()
        
        self.assertEqual(stats['total_readings'], 2)
        self.assertIsNotNone(stats['oldest_record'])
        self.assertIsNotNone(stats['newest_record'])
        self.assertEqual(stats['date_range_days'], 2)
    
    def test_get_sensor_readings_stats_empty(self):
        stats = get_sensor_readings_stats()
        
        self.assertEqual(stats['total_readings'], 0)
        self.assertIsNone(stats['oldest_record'])
        self.assertIsNone(stats['newest_record'])
        self.assertNotIn('date_range_days', stats)


if __name__ == '__main__':
    unittest.main() 