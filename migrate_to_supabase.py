#!/usr/bin/env python3
"""
SQLite to Supabase Migration Script
Migrates all existing data from local SQLite to Supabase PostgreSQL
"""

import os
import sys
import sqlite3
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_sqlite():
    """Connect to local SQLite database"""
    if not os.path.exists('fund_manager.db'):
        logger.error("❌ Local SQLite database 'fund_manager.db' not found!")
        logger.info("💡 Make sure you're in the correct directory and have used the app before.")
        return None
    
    try:
        conn = sqlite3.connect('fund_manager.db')
        conn.row_factory = sqlite3.Row  # Enable column access by name
        logger.info("✅ Connected to SQLite database")
        return conn
    except Exception as e:
        logger.error(f"❌ Failed to connect to SQLite: {e}")
        return None

def connect_to_supabase():
    """Connect to Supabase PostgreSQL database"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        logger.error("❌ DATABASE_URL environment variable not set!")
        logger.info("💡 Set it with: $env:DATABASE_URL = 'your-supabase-connection-string'")
        return None
    
    if not database_url.startswith(('postgresql://', 'postgres://')):
        logger.error("❌ DATABASE_URL doesn't appear to be PostgreSQL!")
        logger.info(f"💡 Current URL starts with: {database_url.split('://')[0] if '://' in database_url else 'unknown'}")
        return None
    
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        # Fix postgres:// URLs
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        logger.info("✅ Connected to Supabase PostgreSQL database")
        return conn
    
    except ImportError:
        logger.error("❌ psycopg2 not installed!")
        logger.info("💡 Install with: pip install psycopg2-binary")
        return None
    except Exception as e:
        logger.error(f"❌ Failed to connect to Supabase: {e}")
        logger.info("💡 Check your DATABASE_URL and Supabase project status")
        return None

def get_table_data(sqlite_conn, table_name):
    """Get all data from a SQLite table"""
    try:
        cursor = sqlite_conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        logger.info(f"📊 Found {len(data)} records in '{table_name}' table")
        return data
    except Exception as e:
        logger.warning(f"⚠️ Error reading from '{table_name}': {e}")
        return []

def migrate_users(sqlite_conn, pg_conn):
    """Migrate users table"""
    logger.info("👥 Migrating users...")
    
    data = get_table_data(sqlite_conn, 'users')
    if not data:
        return
    
    cursor = pg_conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM users")
    
    # Insert data
    for row in data:
        cursor.execute("""
            INSERT INTO users (id, username, password, role) 
            VALUES (%s, %s, %s, %s)
        """, (row['id'], row['username'], row['password'], row['role']))
    
    # Reset sequence
    cursor.execute("SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 1))")
    
    pg_conn.commit()
    logger.info(f"✅ Migrated {len(data)} users")

def migrate_contributors(sqlite_conn, pg_conn):
    """Migrate contributors table"""
    logger.info("🤝 Migrating contributors...")
    
    data = get_table_data(sqlite_conn, 'contributors')
    if not data:
        return
    
    cursor = pg_conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM contributors")
    
    # Insert data
    for row in data:
        cursor.execute("""
            INSERT INTO contributors (id, name, type, login_username) 
            VALUES (%s, %s, %s, %s)
        """, (row['id'], row['name'], row['type'], row['login_username']))
    
    # Reset sequence
    cursor.execute("SELECT setval('contributors_id_seq', COALESCE((SELECT MAX(id) FROM contributors), 1))")
    
    pg_conn.commit()
    logger.info(f"✅ Migrated {len(data)} contributors")

def migrate_transactions(sqlite_conn, pg_conn):
    """Migrate transactions table"""
    logger.info("💰 Migrating transactions...")
    
    data = get_table_data(sqlite_conn, 'transactions')
    if not data:
        return
    
    cursor = pg_conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM transactions")
    
    # Insert data
    for row in data:
        cursor.execute("""
            INSERT INTO transactions (
                id, contributor_id, date, type, amount, purpose,
                trade_symbol, trade_quantity, trade_price, trade_type,
                trade_status, trade_fees, trade_notes, trade_pnl, trade_exit_price
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['id'], row['contributor_id'], row['date'], row['type'], row['amount'],
            row['purpose'], row.get('trade_symbol'), row.get('trade_quantity'), 
            row.get('trade_price'), row.get('trade_type'), row.get('trade_status'),
            row.get('trade_fees'), row.get('trade_notes'), row.get('trade_pnl'), 
            row.get('trade_exit_price')
        ))
    
    # Reset sequence
    cursor.execute("SELECT setval('transactions_id_seq', COALESCE((SELECT MAX(id) FROM transactions), 1))")
    
    pg_conn.commit()
    logger.info(f"✅ Migrated {len(data)} transactions")

def migrate_withdrawal_requests(sqlite_conn, pg_conn):
    """Migrate withdrawal requests table"""
    logger.info("💸 Migrating withdrawal requests...")
    
    data = get_table_data(sqlite_conn, 'withdrawal_requests')
    if not data:
        return
    
    cursor = pg_conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM withdrawal_requests")
    
    # Insert data
    for row in data:
        cursor.execute("""
            INSERT INTO withdrawal_requests (id, contributor_id, amount, status, request_date, admin_notes) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['id'], row['contributor_id'], row['amount'], row['status'], 
              row['request_date'], row.get('admin_notes')))
    
    # Reset sequence
    cursor.execute("SELECT setval('withdrawal_requests_id_seq', COALESCE((SELECT MAX(id) FROM withdrawal_requests), 1))")
    
    pg_conn.commit()
    logger.info(f"✅ Migrated {len(data)} withdrawal requests")

def migrate_trades(sqlite_conn, pg_conn):
    """Migrate trades table"""
    logger.info("📈 Migrating trades...")
    
    data = get_table_data(sqlite_conn, 'trades')
    if not data:
        return
    
    cursor = pg_conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM trades")
    
    # Insert data
    for row in data:
        cursor.execute("""
            INSERT INTO trades (
                id, trade_date, asset, pnl, charges, commission,
                net_pnl, net_profit_after_commission, comment, side,
                quantity, entry_price, exit_price, instrument,
                broker, trade_ref, strategy, tags
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['id'], row['trade_date'], row['asset'], row.get('pnl'), 
            row.get('charges'), row.get('commission'), row.get('net_pnl'),
            row.get('net_profit_after_commission'), row.get('comment'), row.get('side'),
            row.get('quantity'), row.get('entry_price'), row.get('exit_price'),
            row.get('instrument'), row.get('broker'), row.get('trade_ref'),
            row.get('strategy'), row.get('tags')
        ))
    
    # Reset sequence
    cursor.execute("SELECT setval('trades_id_seq', COALESCE((SELECT MAX(id) FROM trades), 1))")
    
    pg_conn.commit()
    logger.info(f"✅ Migrated {len(data)} trades")

def verify_migration(sqlite_conn, pg_conn):
    """Verify migration was successful"""
    logger.info("🔍 Verifying migration...")
    
    tables = ['users', 'contributors', 'transactions', 'withdrawal_requests', 'trades']
    
    for table in tables:
        # Count SQLite records
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table}")
        sqlite_count = sqlite_cursor.fetchone()[0]
        
        # Count PostgreSQL records
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute(f"SELECT COUNT(*) FROM {table}")
        pg_count = pg_cursor.fetchone()[0]
        
        if sqlite_count == pg_count:
            logger.info(f"✅ {table}: {sqlite_count} → {pg_count} ✓")
        else:
            logger.warning(f"⚠️ {table}: {sqlite_count} → {pg_count} (mismatch!)")
    
    logger.info("🔍 Verification completed")

def main():
    print("🚀 SQLite to Supabase Migration")
    print("=" * 50)
    
    # Connect to databases
    logger.info("🔗 Connecting to databases...")
    
    sqlite_conn = connect_to_sqlite()
    if not sqlite_conn:
        sys.exit(1)
    
    pg_conn = connect_to_supabase()
    if not pg_conn:
        sys.exit(1)
    
    try:
        # Ensure Supabase tables exist
        logger.info("🏗️ Setting up Supabase tables...")
        from setup_database import setup_database
        setup_database()
        
        print("\n📋 Starting migration...")
        
        # Migrate all tables
        migrate_users(sqlite_conn, pg_conn)
        migrate_contributors(sqlite_conn, pg_conn)
        migrate_transactions(sqlite_conn, pg_conn)
        migrate_withdrawal_requests(sqlite_conn, pg_conn)
        migrate_trades(sqlite_conn, pg_conn)
        
        # Verify migration
        print()
        verify_migration(sqlite_conn, pg_conn)
        
        print("\n🎉 Migration completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Test your app locally: python app.py")
        print("2. Update Render environment with new DATABASE_URL")
        print("3. Deploy to production")
        print("4. Verify all data appears correctly")
        
        # Show login info
        print("\n🔐 Login credentials remain the same:")
        print("   Username: admin1")
        print("   Password: admin123")
        print("   (Change this after first login!)")
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        sys.exit(1)
    
    finally:
        # Close connections
        if sqlite_conn:
            sqlite_conn.close()
        if pg_conn:
            pg_conn.close()

if __name__ == "__main__":
    main()
