#!/usr/bin/env python3
"""
Data Maintenance Script for Smart Gardening System
Handles data retention and cleanup operations
"""

import sys
import os
import argparse
from datetime import datetime, timedelta, timezone

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smart_gardening.db.database import (
    init_db, 
    cleanup_old_sensor_readings, 
    get_sensor_readings_stats,
    session
)


def run_data_cleanup(retention_days=60, dry_run=False):
    """
    Run data cleanup operation.
    
    Args:
        retention_days: Number of days to keep data
        dry_run: If True, only show what would be deleted without actually deleting
    """
    print(f"🧹 Smart Gardening Data Maintenance")
    print("=" * 50)
    
    # Initialize database
    init_db()
    
    # Get current statistics
    print("📊 Current Database Statistics:")
    stats = get_sensor_readings_stats()
    
    if stats:
        print(f"   Total sensor readings: {stats.get('total_readings', 0)}")
        print(f"   Oldest record: {stats.get('oldest_record', 'N/A')}")
        print(f"   Newest record: {stats.get('newest_record', 'N/A')}")
        if stats.get('date_range_days'):
            print(f"   Date range: {stats['date_range_days']} days")
    else:
        print("   No sensor readings found")
    
    print()
    
    if dry_run:
        print("🔍 DRY RUN MODE - No data will be deleted")
        print("=" * 50)
        
        # Calculate cutoff date
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=retention_days)
        print(f"Would delete records older than: {cutoff_date}")
        
        # Count records that would be deleted
        from smart_gardening.db.database import SensorReading, PumpLog
        
        old_readings = session.query(SensorReading).filter(
            SensorReading.timestamp < cutoff_date
        ).count()
        
        old_pump_logs = session.query(PumpLog).filter(
            PumpLog.timestamp < cutoff_date
        ).count()
        
        print(f"Would delete {old_readings} sensor readings")
        print(f"Would delete {old_pump_logs} pump logs")
        print(f"Total records to be deleted: {old_readings + old_pump_logs}")
        
    else:
        print(f"🗑️  Cleaning up data older than {retention_days} days...")
        print("=" * 50)
        
        # Run cleanup
        deleted_count = cleanup_old_sensor_readings(retention_days)
        
        print(f"✅ Cleanup completed successfully!")
        print(f"   Total records deleted: {deleted_count}")
        
        # Show updated statistics
        print("\n📊 Updated Database Statistics:")
        updated_stats = get_sensor_readings_stats()
        
        if updated_stats:
            print(f"   Remaining sensor readings: {updated_stats.get('total_readings', 0)}")
            print(f"   Oldest record: {updated_stats.get('oldest_record', 'N/A')}")
            print(f"   Newest record: {updated_stats.get('newest_record', 'N/A')}")
            if updated_stats.get('date_range_days'):
                print(f"   Date range: {updated_stats['date_range_days']} days")


def schedule_cleanup():
    """
    Schedule regular cleanup operations.
    This function can be called by a cron job or scheduler.
    """
    print(f"⏰ Scheduled data cleanup at {datetime.now(timezone.utc)}")
    run_data_cleanup(retention_days=60, dry_run=False)


def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(
        description="Smart Gardening Data Maintenance Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --cleanup                    # Run cleanup with default 60-day retention
  %(prog)s --cleanup --days 30          # Run cleanup with 30-day retention
  %(prog)s --cleanup --dry-run          # Show what would be deleted without deleting
  %(prog)s --stats                      # Show database statistics only
  %(prog)s --schedule                   # Run scheduled cleanup (for cron jobs)
        """
    )
    
    parser.add_argument(
        "--cleanup", 
        action="store_true",
        help="Run data cleanup operation"
    )
    
    parser.add_argument(
        "--days", 
        type=int, 
        default=60,
        help="Number of days to keep data (default: 60)"
    )
    
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Show what would be deleted without actually deleting"
    )
    
    parser.add_argument(
        "--stats", 
        action="store_true",
        help="Show database statistics only"
    )
    
    parser.add_argument(
        "--schedule", 
        action="store_true",
        help="Run scheduled cleanup (for cron jobs)"
    )
    
    args = parser.parse_args()
    
    if args.schedule:
        schedule_cleanup()
    elif args.cleanup:
        run_data_cleanup(args.days, args.dry_run)
    elif args.stats:
        print("📊 Smart Gardening Database Statistics")
        print("=" * 50)
        init_db()
        stats = get_sensor_readings_stats()
        
        if stats:
            print(f"Total sensor readings: {stats.get('total_readings', 0)}")
            print(f"Oldest record: {stats.get('oldest_record', 'N/A')}")
            print(f"Newest record: {stats.get('newest_record', 'N/A')}")
            if stats.get('date_range_days'):
                print(f"Date range: {stats['date_range_days']} days")
        else:
            print("No sensor readings found")
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 