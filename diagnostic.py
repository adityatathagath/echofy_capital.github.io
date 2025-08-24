#!/usr/bin/env python3
"""
Quick diagnostic script to check for issues
"""

import os
import sqlite3
import sys

def check_database():
    """Check database integrity"""
    print("🔍 Checking database...")
    
    if not os.path.exists('fund_manager.db'):
        print("❌ Database file not found")
        return False
    
    try:
        conn = sqlite3.connect('fund_manager.db')
        cursor = conn.cursor()
        
        # Check all required tables
        tables = ['users', 'contributors', 'transactions', 'withdrawal_requests', 'trades']
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                print(f"✅ Table '{table}' exists")
            else:
                print(f"❌ Table '{table}' missing")
                return False
        
        # Check admin user
        cursor.execute("SELECT username, role FROM users WHERE role='admin'")
        admin = cursor.fetchone()
        if admin:
            print(f"✅ Admin user exists: {admin[0]}")
        else:
            print("❌ No admin user found")
            return False
        
        conn.close()
        print("✅ Database check passed")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_templates():
    """Check template files"""
    print("\n🔍 Checking templates...")
    
    template_dir = 'templates'
    if not os.path.exists(template_dir):
        print("❌ Templates directory not found")
        return False
    
    required_templates = [
        'base.html', 'login.html', 'dashboard.html', 'manage_contributors.html',
        'add_contributor.html', 'trade_history.html', 'record_trade.html'
    ]
    
    for template in required_templates:
        path = os.path.join(template_dir, template)
        if os.path.exists(path):
            print(f"✅ Template '{template}' exists")
        else:
            print(f"❌ Template '{template}' missing")
            return False
    
    print("✅ Template check passed")
    return True

def check_static_files():
    """Check static files"""
    print("\n🔍 Checking static files...")
    
    static_dir = 'static'
    if not os.path.exists(static_dir):
        print("❌ Static directory not found")
        return False
    
    required_files = ['logo.png']
    for file in required_files:
        path = os.path.join(static_dir, file)
        if os.path.exists(path):
            print(f"✅ Static file '{file}' exists")
        else:
            print(f"⚠️ Static file '{file}' missing (optional)")
    
    print("✅ Static files check completed")
    return True

def check_app_import():
    """Check if app can be imported"""
    print("\n🔍 Checking app import...")
    
    try:
        import app
        print("✅ App module imports successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def main():
    print("🔧 Echofy Capital - Diagnostic Check")
    print("=" * 40)
    
    checks = [
        check_database,
        check_templates,
        check_static_files,
        check_app_import
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All checks passed! No issues found.")
    else:
        print("❌ Some issues found. Check output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
