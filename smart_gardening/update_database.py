#!/usr/bin/env python3
"""
Script to update the existing database with the new last_watered column
"""

import sqlite3
import os

def update_database():
    """Add last_watered column to existing zones table"""
    
    # Path to the database
    db_path = "smart_garden.db"
    
    if not os.path.exists(db_path):
        print(f"Database file {db_path} not found!")
        return
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if last_watered column already exists
        cursor.execute("PRAGMA table_info(zones)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'last_watered' not in columns:
            print("Adding last_watered column to zones table...")
            cursor.execute("ALTER TABLE zones ADD COLUMN last_watered DATETIME")
            conn.commit()
            print("✅ Successfully added last_watered column!")
        else:
            print("✅ last_watered column already exists!")
        
        # Show current table structure
        cursor.execute("PRAGMA table_info(zones)")
        print("\nCurrent zones table structure:")
        for column in cursor.fetchall():
            print(f"  - {column[1]} ({column[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error updating database: {e}")
        if conn:
            conn.close()

if __name__ == "__main__":
    update_database() 