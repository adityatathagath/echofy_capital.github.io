#!/usr/bin/env python3
"""
Universal Database Setup Script
Supports SQLite, PostgreSQL (Supabase, Neon, Railway), and MySQL (PlanetScale)
"""

import os
import sys
import logging
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_database_type(database_url):
    """Determine database type from URL"""
    if not database_url:
        return 'sqlite'
    
    if database_url.startswith('postgresql://') or database_url.startswith('postgres://'):
        return 'postgresql'
    elif database_url.startswith('mysql://'):
        return 'mysql'
    else:
        return 'sqlite'

def create_postgresql_tables(cursor):
    """Create tables for PostgreSQL (Supabase, Neon, Railway)"""
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)
    
    # Contributors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contributors (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            type TEXT NOT NULL,
            login_username TEXT UNIQUE
        )
    """)
    
    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
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
    
    # Withdrawal requests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS withdrawal_requests (
            id SERIAL PRIMARY KEY,
            contributor_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            request_date TEXT NOT NULL,
            admin_notes TEXT,
            FOREIGN KEY (contributor_id) REFERENCES contributors (id) ON DELETE CASCADE
        )
    """)
    
    # Trades table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
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

def create_mysql_tables(cursor):
    """Create tables for MySQL (PlanetScale)"""
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role VARCHAR(50) NOT NULL DEFAULT 'user'
        )
    """)
    
    # Contributors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contributors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            type VARCHAR(100) NOT NULL,
            login_username VARCHAR(255) UNIQUE
        )
    """)
    
    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            contributor_id INT NOT NULL,
            date TEXT NOT NULL,
            type VARCHAR(50) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            purpose TEXT,
            trade_symbol VARCHAR(20),
            trade_quantity DECIMAL(10,4),
            trade_price DECIMAL(10,4),
            trade_type VARCHAR(20),
            trade_status VARCHAR(20),
            trade_fees DECIMAL(10,2),
            trade_notes TEXT,
            trade_pnl DECIMAL(10,2),
            trade_exit_price DECIMAL(10,4),
            FOREIGN KEY (contributor_id) REFERENCES contributors (id) ON DELETE CASCADE
        )
    """)
    
    # Withdrawal requests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS withdrawal_requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            contributor_id INT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            request_date TEXT NOT NULL,
            admin_notes TEXT,
            FOREIGN KEY (contributor_id) REFERENCES contributors (id) ON DELETE CASCADE
        )
    """)
    
    # Trades table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INT AUTO_INCREMENT PRIMARY KEY,
            trade_date TEXT NOT NULL,
            asset VARCHAR(50) NOT NULL,
            pnl DECIMAL(10,2),
            charges DECIMAL(10,2),
            commission DECIMAL(10,2),
            net_pnl DECIMAL(10,2),
            net_profit_after_commission DECIMAL(10,2),
            comment TEXT,
            side VARCHAR(10),
            quantity DECIMAL(10,4),
            entry_price DECIMAL(10,4),
            exit_price DECIMAL(10,4),
            instrument VARCHAR(50),
            broker VARCHAR(50),
            trade_ref VARCHAR(100),
            strategy VARCHAR(100),
            tags TEXT
        )
    """)

def create_sqlite_tables(cursor):
    """Create tables for SQLite (local development)"""
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)
    
    # Contributors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contributors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            type TEXT NOT NULL,
            login_username TEXT UNIQUE
        )
    """)
    
    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
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
    
    # Withdrawal requests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS withdrawal_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contributor_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            request_date TEXT NOT NULL,
            admin_notes TEXT,
            FOREIGN KEY (contributor_id) REFERENCES contributors (id) ON DELETE CASCADE
        )
    """)
    
    # Trades table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
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

def setup_database():
    """Setup database based on DATABASE_URL or default to SQLite"""
    
    database_url = os.environ.get('DATABASE_URL')
    db_type = get_database_type(database_url)
    
    logger.info(f"🔧 Setting up {db_type.upper()} database...")
    
    try:
        if db_type == 'postgresql':
            # PostgreSQL (Supabase, Neon, Railway)
            import psycopg2
            from psycopg2.extras import RealDictCursor
            
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            
            conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            
            create_postgresql_tables(cursor)
            
            # Create admin user
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
            admin_count = cursor.fetchone()[0]
            
            if admin_count == 0:
                admin_password = generate_password_hash("admin123")
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                    ("admin1", admin_password, "admin")
                )
                logger.info("✅ Created admin user: admin1")
            
            conn.commit()
            conn.close()
            logger.info("✅ PostgreSQL database setup completed!")
            
        elif db_type == 'mysql':
            # MySQL (PlanetScale)
            import pymysql
            
            # Parse MySQL URL
            from urllib.parse import urlparse
            parsed = urlparse(database_url)
            
            conn = pymysql.connect(
                host=parsed.hostname,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path[1:],  # Remove leading slash
                port=parsed.port or 3306,
                charset='utf8mb4'
            )
            cursor = conn.cursor()
            
            create_mysql_tables(cursor)
            
            # Create admin user
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
            admin_count = cursor.fetchone()[0]
            
            if admin_count == 0:
                admin_password = generate_password_hash("admin123")
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                    ("admin1", admin_password, "admin")
                )
                logger.info("✅ Created admin user: admin1")
            
            conn.commit()
            conn.close()
            logger.info("✅ MySQL database setup completed!")
            
        else:
            # SQLite (local development)
            conn = sqlite3.connect('fund_manager.db')
            cursor = conn.cursor()
            
            create_sqlite_tables(cursor)
            
            # Create admin user
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
            admin_count = cursor.fetchone()[0]
            
            if admin_count == 0:
                admin_password = generate_password_hash("admin123")
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    ("admin1", admin_password, "admin")
                )
                logger.info("✅ Created admin user: admin1")
            
            conn.commit()
            conn.close()
            logger.info("✅ SQLite database setup completed!")
        
        logger.info("🎉 Database setup successful!")
        logger.info("🔐 Default login: admin1 / admin123")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        return False

def main():
    print("🗄️ Universal Database Setup")
    print("=" * 50)
    
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        db_type = get_database_type(database_url)
        print(f"📍 Target: {db_type.upper()} database")
        if 'postgresql' in database_url:
            if 'supabase' in database_url:
                print("🟢 Provider: Supabase")
            elif 'neon' in database_url:
                print("🟢 Provider: Neon")
            elif 'railway' in database_url:
                print("🟢 Provider: Railway") 
            else:
                print("🟢 Provider: PostgreSQL")
        elif 'planetscale' in database_url:
            print("🟢 Provider: PlanetScale")
    else:
        print("📍 Target: SQLite (local development)")
    
    print("")
    
    success = setup_database()
    
    if success:
        print("\n🎉 SUCCESS: Database ready for production!")
        print("\n📋 Next Steps:")
        print("1. Test the application: python app.py")
        print("2. Deploy to Render with new DATABASE_URL")
        print("3. Change admin password after first login")
    else:
        print("\n❌ Setup failed. Check logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
