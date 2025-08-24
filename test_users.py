#!/usr/bin/env python3
"""Test database users"""

import app

with app.app.app_context():
    db = app.get_db()
    users = db.get_all_users()
    print('Users in database:')
    for user in users:
        print(f"  - Username: {user['username']}, Role: {user['role']}")
    print(f'Total users: {len(users)}')
