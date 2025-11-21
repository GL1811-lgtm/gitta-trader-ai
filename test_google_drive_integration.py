"""
Test Google Drive Service Integration
Validates credentials, connection, and basic operations
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.google_drive_service import GoogleDriveService
from backend.config import config


def test_google_drive():
    """Test Google Drive service"""
    
    print("=" * 70)
    print("TESTING GOOGLE DRIVE SERVICE")
    print("=" * 70)
    
    # Test 1: Configuration
    print("\n📋 Test 1: Configuration Check")
    print("-" * 70)
    print(f"Credentials Path: {config.GOOGLE_DRIVE_CREDENTIALS_PATH}")
    print(f"Folder ID:        {config.GOOGLE_DRIVE_FOLDER_ID}")
    print(f"Backups Enabled:  {config.BACKUP_ENABLED}")
    
    if not os.path.exists(config.GOOGLE_DRIVE_CREDENTIALS_PATH):
        print(f"\n❌ FAILED: Credentials file not found")
        print(f"   Expected at: {config.GOOGLE_DRIVE_CREDENTIALS_PATH}")
        return False
    
    if not config.GOOGLE_DRIVE_FOLDER_ID:
        print(f"\n❌ FAILED: GOOGLE_DRIVE_FOLDER_ID not set in .env")
        print("   Please add: GOOGLE_DRIVE_FOLDER_ID=your_folder_id")
        return False
    
    print("✅ Configuration is valid")
    
    # Test 2: Initialize Service
    print("\n🔌 Test 2: Initialize Service")
    print("-" * 70)
    
    try:
        drive = GoogleDriveService()
        
        if not drive.connected:
            print("❌ FAILED: Could not connect to Google Drive")
            return False
        
        print("✅ Successfully connected to Google Drive")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 3: Get Storage Info
    print("\n📊 Test 3: Storage Information")
    print("-" * 70)
    
    try:
        info = drive.get_storage_info()
        print(f"Total Files:  {info['total_files']}")
        print(f"Total Size:   {info['total_size_mb']:.2f} MB ({info['total_size_gb']:.4f} GB)")
        print(f"Folder ID:    {info['folder_id']}")
        print("✅ Storage info retrieved")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 4: List Backups
    print("\n📂 Test 4: List Existing Backups")
    print("-" * 70)
    
    try:
        backups = drive.list_backups()
        
        if backups:
            print(f"Found {len(backups)} file(s) in Google Drive folder:")
            for i, backup in enumerate(backups[:5], 1):  # Show first 5
                size_mb = int(backup.get('size', 0)) / (1024 * 1024)
                created = backup.get('createdTime', 'Unknown')[:10]
                print(f"  {i}. {backup['name'][:50]}")
                print(f"     Size: {size_mb:.2f} MB | Created: {created}")
        else:
            print("No backups found (this is normal for first-time setup)")
        
        print("✅ Backup listing successful")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 5: Upload Test File
    print("\n📤 Test 5: Upload Test File")
    print("-" * 70)
    
    try:
        # Create a test file
        test_file_path = "test_upload.txt"
        with open(test_file_path, 'w') as f:
            f.write(f"Test upload from Gitta Trader AI\nTimestamp: {os.popen('date').read()}")
        
        # Upload
        file_id = drive.upload_file(test_file_path, "gitta_test_upload.txt")
        
        if file_id:
            print(f"✅ Test file uploaded successfully!")
            print(f"   File ID: {file_id}")
            
            # Clean up test file locally
            os.remove(test_file_path)
            
            # Delete test file from Drive
            print("\n🗑️  Cleaning up test file from Drive...")
            if drive.delete_file(file_id):
                print("✅ Test file cleaned up")
        else:
            print("❌ Upload failed")
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
            return False
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        # Clean up
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
        return False
    
    # Test 6: Database Backup (if database exists)
    print("\n💾 Test 6: Database Backup")
    print("-" * 70)
    
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'backend', 'data', 'gitta.db'
    )
    
    if os.path.exists(db_path):
        try:
            print(f"Database found at: {db_path}")
            print(f"Database size: {os.path.getsize(db_path) / (1024*1024):.2f} MB")
            
            # Perform backup
            print("\nBacking up database...")
            file_id = drive.backup_database(db_path)
            
            if file_id:
                print("✅ Database backup successful!")
                print(f"   File ID: {file_id}")
                print("\n⚠️  Note: This backup will be kept. Run cleanup manually if needed.")
            else:
                print("❌ Database backup failed")
                return False
                
        except Exception as e:
            print(f"❌ FAILED: {e}")
            return False
    else:
        print("⚠️  Database file not found - skipping database backup test")
        print("   This is normal if you haven't run the system yet")
    
    # Final Summary
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nGoogle Drive is fully configured and working!")
    print("\nNext steps:")
    print("1. Database backups will run automatically at 11 PM daily")
    print("2. You can manually trigger backups using:")
    print("   python -c 'from backend.services.google_drive_service import backup_now; backup_now()'")
    print("3. View backups anytime at: https://drive.google.com")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    success = test_google_drive()
    sys.exit(0 if success else 1)
