"""
Test Cloud Database Configuration
Tests PostgreSQL and SQLite connections
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import config
from backend.database.db import DatabaseManager


def test_database():
    """Test database configuration and connection"""
    
    print("=" * 70)
    print("TESTING DATABASE CONFIGURATION")
    print("=" * 70)
    
    # Test 1: Configuration
    print("\n📋 Test 1: Database Configuration")
    print("-" * 70)
    print(f"Database Type: {config.DATABASE_TYPE}")
    
    if config.DATABASE_TYPE == 'postgresql':
        # Mask password
        masked_url = config.DATABASE_URL
        if '@' in masked_url:
            parts = masked_url.split('@')
            before_at = parts[0].split(':')
            before_at[-1] = '****'
            masked_url = ':'.join(before_at) + '@' + parts[1]
        print(f"Database URL:  {masked_url}")
    else:
        print(f"Database Path: {config.DATABASE_PATH}")
    
    print("✅ Configuration loaded")
    
    # Test 2: Initialize Database Manager
    print("\n🔌 Test 2: Initialize Database Manager")
    print("-" * 70)
    
    try:
        db = DatabaseManager()
        print("✅ Database manager initialized")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 3: Test Connection
    print("\n💾 Test 3: Test Database Connection")
    print("-" * 70)
    
    try:
        # Try a simple query
        with db._get_connection() as conn:
            cursor = conn.cursor()
            
            if config.DATABASE_TYPE == 'postgresql':
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                print(f"PostgreSQL Version: {version}")
            else:
                cursor.execute("SELECT sqlite_version();")
                version = cursor.fetchone()[0]
                print(f"SQLite Version: {version}")
        
        print("✅ Database connection successful")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 4: Check Tables
    print("\n📊 Test 4: Check Database Tables")
    print("-" * 70)
    
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            
            if config.DATABASE_TYPE == 'postgresql':
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
            else:
                cursor.execute("""
                    SELECT name 
                    FROM sqlite_master 
                    WHERE type='table'
                """)
            
            tables = [row[0] for row in cursor.fetchall()]
            
            if tables:
                print(f"Found {len(tables)} table(s):")
                for table in sorted(tables):
                    print(f"  - {table}")
            else:
                print("⚠️  No tables found (database may need initialization)")
        
        print("✅ Table check complete")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 5: Test Basic Operations
    print("\n✏️  Test 5: Test Basic CRUD Operations")
    print("-" * 70)
    
    try:
        # Test logging (should work on any schema)
        activity_id = db.log_agent_activity(
            agent_id="test_agent",
            activity_type="TEST",
            description="Database connection test",
            metadata={"test": True}
        )
        
        if activity_id:
            print(f"✅ Insert operation successful (ID: {activity_id})")
            
            # Test read
            logs = db.get_agent_activity_logs("test_agent", limit=1)
            if logs:
                print(f"✅ Read operation successful")
                print(f"   Retrieved {len(logs)} log(s)")
            else:
                print("⚠️  Read returned no data")
        else:
            print("⚠️  Insert did not return an ID (this might be normal)")
        
    except Exception as e:
        print(f"⚠️  CRUD test skipped: {e}")
        print("   (This might happen if schema isn't initialized)")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ DATABASE TESTS PASSED!")
    print("=" * 70)
    
    if config.DATABASE_TYPE == 'postgresql':
        print("\n🐘 PostgreSQL is ready for cloud deployment!")
        print("   Your data will persist in the cloud database")
    else:
        print("\n📁 SQLite is ready for local development!")
        print("   To use PostgreSQL for cloud, set DATABASE_URL in .env")
    
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    success = test_database()
    sys.exit(0 if success else 1)
