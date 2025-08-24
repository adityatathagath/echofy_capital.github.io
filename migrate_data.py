#!/usr/bin/env python3
"""
Database migration script for transitioning from SQLite to PostgreSQL
"""

import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_sqlite_to_postgres():
    """Migrate data from SQLite to PostgreSQL"""
    
    # Get database URLs
    sqlite_path = os.environ.get('SQLITE_DB_PATH', 'fund_manager.db')
    postgres_url = os.environ.get('DATABASE_URL')
    
    if not postgres_url:
        logger.error("DATABASE_URL environment variable not set")
        return False
    
    if not os.path.exists(sqlite_path):
        logger.info(f"SQLite database {sqlite_path} not found, skipping migration")
        return True
    
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_conn.row_factory = sqlite3.Row
        
        # Connect to PostgreSQL
        if postgres_url.startswith('postgres://'):
            postgres_url = postgres_url.replace('postgres://', 'postgresql://', 1)
        
        postgres_conn = psycopg2.connect(postgres_url, cursor_factory=RealDictCursor)
        
        logger.info("Connected to both databases")
        
        # Migrate users table
        logger.info("Migrating users table...")
        sqlite_cursor = sqlite_conn.execute("SELECT * FROM users")
        users = sqlite_cursor.fetchall()
        
        postgres_cursor = postgres_conn.cursor()
        for user in users:
            postgres_cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s) ON CONFLICT (username) DO NOTHING",
                (user['username'], user['password'], user['role'])
            )
        
        # Migrate contributors table
        logger.info("Migrating contributors table...")
        sqlite_cursor = sqlite_conn.execute("SELECT * FROM contributors")
        contributors = sqlite_cursor.fetchall()
        
        for contrib in contributors:
            postgres_cursor.execute(
                "INSERT INTO contributors (name, type, login_username) VALUES (%s, %s, %s) ON CONFLICT (name) DO NOTHING",
                (contrib['name'], contrib['type'], contrib['login_username'])
            )
        
        # Migrate transactions table
        logger.info("Migrating transactions table...")
        sqlite_cursor = sqlite_conn.execute("SELECT * FROM transactions")
        transactions = sqlite_cursor.fetchall()
        
        for txn in transactions:
            postgres_cursor.execute("""
                INSERT INTO transactions 
                (contributor_id, date, type, amount, purpose, trade_symbol, trade_quantity, 
                 trade_price, trade_type, trade_status, trade_fees, trade_notes, trade_pnl, trade_exit_price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                txn['contributor_id'], txn['date'], txn['type'], txn['amount'],
                txn.get('purpose', ''), txn.get('trade_symbol', ''), txn.get('trade_quantity', 0),
                txn.get('trade_price', 0), txn.get('trade_type', ''), txn.get('trade_status', ''),
                txn.get('trade_fees', 0), txn.get('trade_notes', ''), txn.get('trade_pnl', 0),
                txn.get('trade_exit_price', 0)
            ))
        
        # Migrate withdrawal requests table
        logger.info("Migrating withdrawal requests table...")
        sqlite_cursor = sqlite_conn.execute("SELECT * FROM withdrawal_requests")
        withdrawal_requests = sqlite_cursor.fetchall()
        
        for req in withdrawal_requests:
            postgres_cursor.execute("""
                INSERT INTO withdrawal_requests 
                (contributor_id, amount, status, request_date, admin_notes)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                req['contributor_id'], req['amount'], req['status'],
                req['request_date'], req.get('admin_notes', '')
            ))
        
        # Commit all changes
        postgres_conn.commit()
        logger.info("Migration completed successfully")
        
        # Close connections
        sqlite_conn.close()
        postgres_conn.close()
        
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        if 'postgres_conn' in locals():
            postgres_conn.rollback()
            postgres_conn.close()
        if 'sqlite_conn' in locals():
            sqlite_conn.close()
        return False

def create_postgres_tables():
    """Create tables in PostgreSQL database"""
    
    postgres_url = os.environ.get('DATABASE_URL')
    if not postgres_url:
        logger.error("DATABASE_URL environment variable not set")
        return False
    
    try:
        if postgres_url.startswith('postgres://'):
            postgres_url = postgres_url.replace('postgres://', 'postgresql://', 1)
        
        postgres_conn = psycopg2.connect(postgres_url, cursor_factory=RealDictCursor)
        postgres_cursor = postgres_conn.cursor()
        
        # Create tables with PostgreSQL syntax
        postgres_cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        """)
        
        postgres_cursor.execute("""
            CREATE TABLE IF NOT EXISTS contributors (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE,
                type TEXT,
                login_username TEXT
            )
        """)
        
        postgres_cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                contributor_id INTEGER,
                date TEXT,
                type TEXT,
                amount REAL,
                purpose TEXT,
                trade_symbol TEXT,
                trade_quantity REAL,
                trade_price REAL,
                trade_type TEXT,
                trade_status TEXT,
                trade_fees REAL,
                trade_notes TEXT,
                trade_pnl REAL,
                trade_exit_price REAL,
                FOREIGN KEY (contributor_id) REFERENCES contributors (id)
            )
        """)
        
        postgres_cursor.execute("""
            CREATE TABLE IF NOT EXISTS withdrawal_requests (
                id SERIAL PRIMARY KEY,
                contributor_id INTEGER,
                amount REAL,
                status TEXT DEFAULT 'pending',
                request_date TEXT,
                admin_notes TEXT,
                FOREIGN KEY (contributor_id) REFERENCES contributors (id)
            )
        """)
        
        # Create trades table if it doesn't exist
        postgres_cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id SERIAL PRIMARY KEY,
                trade_date TEXT,
                asset TEXT,
                pnl REAL,
                charges REAL,
                commission REAL,
                net_pnl REAL,
                net_profit_after_commission REAL,
                comment TEXT,
                side TEXT,
                quantity REAL,
                entry_price REAL,
                exit_price REAL,
                instrument TEXT,
                broker TEXT,
                trade_ref TEXT,
                strategy TEXT,
                tags TEXT
            )
        """)
        
        postgres_conn.commit()
        postgres_conn.close()
        
        logger.info("PostgreSQL tables created successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create PostgreSQL tables: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting database migration...")
    
    # First create tables
    if create_postgres_tables():
        # Then migrate data
        if migrate_sqlite_to_postgres():
            logger.info("Database migration completed successfully!")
        else:
            logger.error("Data migration failed!")
    else:
        logger.error("Table creation failed!")
