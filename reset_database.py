#!/usr/bin/env python3
"""
Database Reset Script for Production Launch
This script completely resets the database to a clean state with only the admin account.
"""

import os
import sqlite3
import logging
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_sqlite_database():
    """Reset SQLite database to clean state"""
    db_path = 'fund_manager.db'
    
    if not os.path.exists(db_path):
        logger.info(f"Database {db_path} not found. Will create fresh database.")
    else:
        logger.info(f"Found existing database {db_path}. Will reset completely.")
    
    try:
        # Remove existing database
        if os.path.exists(db_path):
            os.remove(db_path)
            logger.info("✅ Removed existing database file")
        
        # Create fresh database connection
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        
        logger.info("🚀 Creating fresh database schema...")
        
        # Users table
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            )
        """)
        logger.info("✅ Created users table")
        
        # Contributors table
        cursor.execute("""
            CREATE TABLE contributors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL,
                login_username TEXT UNIQUE
            )
        """)
        logger.info("✅ Created contributors table")
        
        # Transactions table
        cursor.execute("""
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contributor_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
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
                FOREIGN KEY (contributor_id) REFERENCES contributors (id) ON DELETE CASCADE
            )
        """)
        logger.info("✅ Created transactions table")
        
        # Withdrawal requests table
        cursor.execute("""
            CREATE TABLE withdrawal_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contributor_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                request_date TEXT NOT NULL,
                admin_notes TEXT,
                FOREIGN KEY (contributor_id) REFERENCES contributors (id) ON DELETE CASCADE
            )
        """)
        logger.info("✅ Created withdrawal_requests table")
        
        # Trades table
        cursor.execute("""
            CREATE TABLE trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trade_date TEXT NOT NULL,
                asset TEXT NOT NULL,
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
        logger.info("✅ Created trades table")
        
        # Insert only the default admin account
        admin_password_hash = generate_password_hash("admin123")
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin1", admin_password_hash, "admin")
        )
        logger.info("✅ Created default admin account")
        
        # Commit all changes
        conn.commit()
        conn.close()
        
        # Log database statistics
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM contributors")  
        contributor_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM transactions")
        transaction_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM withdrawal_requests")
        withdrawal_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM trades")
        trades_count = cursor.fetchone()[0]
        
        conn.close()
        
        logger.info("🎉 Database reset completed successfully!")
        logger.info(f"📊 Database Statistics:")
        logger.info(f"   Users: {user_count}")
        logger.info(f"   Contributors: {contributor_count}")
        logger.info(f"   Transactions: {transaction_count}")
        logger.info(f"   Withdrawal Requests: {withdrawal_count}")
        logger.info(f"   Trades: {trades_count}")
        logger.info("")
        logger.info("🔐 Default Login Credentials:")
        logger.info("   Username: admin1")
        logger.info("   Password: admin123")
        logger.info("")
        logger.info("⚠️  IMPORTANT: Change the admin password after first login!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error resetting database: {e}")
        return False

def reset_production_database():
    """Reset production PostgreSQL database (for Render deployment)"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        logger.info("No DATABASE_URL found. Skipping production database reset.")
        return True
    
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        logger.info("🚀 Resetting production PostgreSQL database...")
        
        # Drop all tables if they exist
        tables = ['withdrawal_requests', 'transactions', 'trades', 'contributors', 'users']
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
            logger.info(f"✅ Dropped {table} table")
        
        # Recreate tables with PostgreSQL syntax
        cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            )
        """)
        
        cursor.execute("""
            CREATE TABLE contributors (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL,
                login_username TEXT UNIQUE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE transactions (
                id SERIAL PRIMARY KEY,
                contributor_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
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
                FOREIGN KEY (contributor_id) REFERENCES contributors (id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE withdrawal_requests (
                id SERIAL PRIMARY KEY,
                contributor_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                request_date TEXT NOT NULL,
                admin_notes TEXT,
                FOREIGN KEY (contributor_id) REFERENCES contributors (id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE trades (
                id SERIAL PRIMARY KEY,
                trade_date TEXT NOT NULL,
                asset TEXT NOT NULL,
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
        
        # Insert default admin account
        admin_password_hash = generate_password_hash("admin123")
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            ("admin1", admin_password_hash, "admin")
        )
        
        conn.commit()
        conn.close()
        
        logger.info("🎉 Production database reset completed successfully!")
        return True
        
    except ImportError:
        logger.warning("psycopg2 not available. Skipping production database reset.")
        return True
    except Exception as e:
        logger.error(f"❌ Error resetting production database: {e}")
        return False

def main():
    """Main function to reset database"""
    print("🗄️  Database Reset Script")
    print("=" * 50)
    print("This will completely reset your database to a clean state.")
    print("⚠️  WARNING: This will delete ALL existing data!")
    print("")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--confirm":
        logger.info("Starting database reset...")
        
        # Reset local SQLite database
        success_local = reset_sqlite_database()
        
        # Reset production database if DATABASE_URL is set
        success_prod = reset_production_database()
        
        if success_local and success_prod:
            print("")
            print("🎉 SUCCESS: Database reset completed!")
            print("🚀 Your application is ready for production launch!")
            print("")
            print("📋 Next Steps:")
            print("1. Test the application locally")
            print("2. Commit and push changes to GitHub")
            print("3. Deploy to Render")
            print("4. Change admin password after first login")
        else:
            print("❌ Database reset failed. Check logs above.")
            sys.exit(1)
    else:
        print("Usage: python reset_database.py --confirm")
        print("")
        print("Add --confirm flag to proceed with the database reset.")

if __name__ == "__main__":
    main()
