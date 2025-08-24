#!/usr/bin/env python3
"""Test script to isolate Flask application issues"""

import os
import sys
import traceback

print("Starting app test...")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

try:
    print("Attempting to import Flask...")
    from flask import Flask
    print("✓ Flask imported successfully")
    
    print("Attempting to import app module...")
    import app
    print("✓ app module imported successfully")
    
    print("Attempting to access Flask app...")
    flask_app = app.app
    print("✓ Flask app accessed successfully")
    
    print("Attempting to run Flask app in test mode...")
    with flask_app.app_context():
        print("✓ App context created successfully")
        
    print("Attempting to create database connection...")
    from app import get_db
    with flask_app.app_context():
        db = get_db()
        print("✓ Database connection established")
    
    print("All tests passed! App should be working.")
    
except Exception as e:
    print(f"❌ Error occurred: {e}")
    print("Full traceback:")
    traceback.print_exc()
