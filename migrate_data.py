#!/usr/bin/env python3
"""
Migration script to move data from SQLite to PostgreSQL for Render deployment
Run this script to migrate your existing data when switching to PostgreSQL
"""

import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import sys

def migrate_data():
    """Migrate data from SQLite to PostgreSQL"""
    
    # Source SQLite database
    sqlite_db = 'fund_manager.db'
    if not os.path.exists(sqlite_db):
        print(f"SQLite database {sqlite_db} not found!")
        return False
    
    # Target PostgreSQL database (from environment)
    postgres_url = os.environ.get('DATABASE_URL')
    if not postgres_url:
        print("DATABASE_URL environment variable not set!")
        print("Please set it to your PostgreSQL connection string")
        return False
    
    if postgres_url.startswith('postgres://'):
        postgres_url = postgres_url.replace('postgres://', 'postgresql://', 1)
    
    print("Starting data migration from SQLite to PostgreSQL...")
    
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_db)
        sqlite_conn.row_factory = sqlite3.Row
        
        # Connect to PostgreSQL
        pg_conn = psycopg2.connect(postgres_url, cursor_factory=RealDictCursor)
        
        # Get cursors
        sqlite_cur = sqlite_conn.cursor()
        pg_cur = pg_conn.cursor()
        
        print("✓ Connected to both databases")
        
        # Tables to migrate
        tables = ['users', 'contributors', 'transactions', 'withdrawal_requests']
        
        for table in tables:
            print(f"Migrating {table}...")
            
            # Get data from SQLite
            sqlite_cur.execute(f"SELECT * FROM {table}")
            rows = sqlite_cur.fetchall()
            
            if not rows:
                print(f"  No data in {table}")
                continue
            
            # Clear existing data in PostgreSQL (optional - remove if you want to keep existing data)
            pg_cur.execute(f"DELETE FROM {table}")
            
            # Insert data into PostgreSQL
            for row in rows:
                columns = list(row.keys())
                values = list(row)
                
                # Handle the id column - don't insert it for SERIAL columns
                if 'id' in columns and table in ['users', 'contributors', 'transactions', 'withdrawal_requests']:
                    id_index = columns.index('id')
                    columns.pop(id_index)
                    values.pop(id_index)
                
                if columns and values:
                    placeholders = ', '.join(['%s'] * len(values))
                    column_names = ', '.join(columns)
                    
                    query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
                    pg_cur.execute(query, values)
            
            print(f"  ✓ Migrated {len(rows)} rows from {table}")
        
        # Commit all changes
        pg_conn.commit()
        
        # Close connections
        sqlite_conn.close()
        pg_conn.close()
        
        print("✅ Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--confirm":
        migrate_data()
    else:
        print("Data Migration Script")
        print("====================")
        print("This script will migrate data from SQLite to PostgreSQL")
        print("Make sure to set the DATABASE_URL environment variable first")
        print()
        print("Usage: python migrate_data.py --confirm")
        print()
        print("WARNING: This will replace all data in the PostgreSQL database!")
