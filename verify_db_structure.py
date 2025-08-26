# -*- coding: utf-8 -*-
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_db_structure():
    try:
        conn = sqlite3.connect('fund_manager.db')
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        logger.info("Found tables: %s", table_names)
        
        # Expected tables
        expected_tables = {
            'users',
            'contributors',
            'transactions',
            'withdrawal_requests',
            'trades'
        }
        
        # Check if all expected tables exist
        missing_tables = expected_tables - set(table_names)
        if missing_tables:
            logger.error("Missing tables: %s", missing_tables)
            return False
            
        # Verify table structures
        for table in table_names:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            logger.info("\nTable '%s' structure:", table)
            for col in columns:
                logger.info("  Column: %s, Type: %s", col[1], col[2])
        
        logger.info("✅ Database structure verification complete!")
        return True
        
    except Exception as e:
        logger.error("❌ Verification failed: %s", str(e))
        return False
        
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    verify_db_structure()
