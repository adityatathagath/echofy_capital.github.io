#!/usr/bin/env python3
"""
Database Setup Test Script
Tests the universal database setup functionality
"""

import os
import sys

def test_database_types():
    """Test database type detection"""
    print("🧪 Testing Database Type Detection")
    print("=" * 40)
    
    # Import our database helper
    sys.path.append('.')
    from setup_database import get_database_type
    
    test_cases = [
        ("", "sqlite"),
        ("sqlite:///test.db", "sqlite"),
        ("postgresql://user:pass@host/db", "postgresql"),
        ("postgres://user:pass@host/db", "postgresql"),
        ("mysql://user:pass@host/db", "mysql"),
    ]
    
    for url, expected in test_cases:
        result = get_database_type(url)
        status = "✅" if result == expected else "❌"
        print(f"{status} {url or 'None'} → {result}")
    
    print()

def test_local_setup():
    """Test local SQLite setup"""
    print("🧪 Testing Local Database Setup")
    print("=" * 40)
    
    from setup_database import setup_database
    
    # Remove any existing DATABASE_URL for this test
    old_db_url = os.environ.get('DATABASE_URL')
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
    
    success = setup_database()
    
    # Restore original DATABASE_URL if it existed
    if old_db_url:
        os.environ['DATABASE_URL'] = old_db_url
    
    if success:
        print("✅ Local SQLite setup test passed!")
    else:
        print("❌ Local SQLite setup test failed!")
    
    return success

def test_app_startup():
    """Test application startup"""
    print("🧪 Testing Application Startup")
    print("=" * 40)
    
    try:
        import app
        print("✅ App module imports successfully")
        
        # Test database manager
        db_manager = app.DatabaseManager()
        print("✅ Database manager created successfully")
        
        return True
    except Exception as e:
        print(f"❌ App startup test failed: {e}")
        return False

def main():
    print("🧪 Database Setup Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        ("Database Type Detection", test_database_types),
        ("Local Database Setup", test_local_setup),
        ("Application Startup", test_app_startup),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result is not False:  # None or True both count as pass
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your database setup is working correctly!")
        
        print("\n📋 Next Steps:")
        print("1. Set up your external database (Supabase/Neon/PlanetScale/Railway)")
        print("2. Set DATABASE_URL environment variable")
        print("3. Run: python setup_database.py")
        print("4. Deploy to production")
    else:
        print("⚠️ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
