"""
Interactive Setup Wizard for Google Drive Integration
Guides user through the complete setup process
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_step(number, text):
    """Print step number"""
    print(f"\n{'='*70}")
    print(f"STEP {number}: {text}")
    print('='*70 + "\n")


def check_credentials_file():
    """Check if credentials.json exists"""
    print_step(1, "Check Credentials File")
    
    creds_path = "credentials.json"
    
    if os.path.exists(creds_path):
        print(f"✅ Found credentials file: {creds_path}")
        
        # Validate JSON
        try:
            with open(creds_path, 'r') as f:
                creds = json.load(f)
            
            # Check for service account
            if creds.get('type') == 'service_account':
                print(f"✅ Valid service account credentials")
                print(f"   Project:        {creds.get('project_id', 'Unknown')}")
                print(f"   Service Email:  {creds.get('client_email', 'Unknown')}")
                return True, creds
            else:
                print(f"❌ Not a service account file")
                return False, None
                
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON file")
            return False, None
    else:
        print(f"❌ Credentials file not found: {creds_path}")
        print("\n📋 To create credentials.json:")
        print("   1. Go to https://console.cloud.google.com/")
        print("   2. Create or select a project")
        print("   3. Enable Google Drive API")
        print("   4. Create Service Account credentials")
        print("   5. Download JSON key file")
        print("   6. Save it as 'credentials.json' in this directory")
        print(f"\nExpected location: {os.path.abspath(creds_path)}")
        return False, None


def get_folder_id():
    """Get and validate Google Drive folder ID"""
    print_step(2, "Get Google Drive Folder ID")
    
    print("You need to create a folder in Google Drive and share it with the service account.")
    print("")
    
    # Check if it's already in .env
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('GOOGLE_DRIVE_FOLDER_ID='):
                    folder_id = line.split('=')[1].strip()
                    if folder_id and folder_id != "your_folder_id_here":
                        print(f"✅ Found folder ID in .env: {folder_id}")
                        
                        use_existing = input("\nUse this folder ID? (y/n): ").strip().lower()
                        if use_existing == 'y':
                            return folder_id
    
    print("\n📋 To get your folder ID:")
    print("   1. Go to https://drive.google.com")
    print("   2. Create a new folder (e.g., 'Gitta-Trader-Backups')")
    print("   3. Right-click the folder → Share")
    print("   4. Add the service account email (from credentials.json)")
    print("   5. Give it 'Editor' permission")
    print("   6. Open the folder and copy the ID from the URL")
    print("      URL format: https://drive.google.com/drive/folders/[FOLDER_ID]")
    print("")
    
    folder_id = input("Enter your Google Drive Folder ID: ").strip()
    
    if not folder_id:
        print("❌ Folder ID is required")
        return None
    
    print(f"✅ Folder ID: {folder_id}")
    return folder_id


def update_env_file(folder_id):
    """Update .env file with configuration"""
    print_step(3, "Update .env File")
    
    env_path = ".env"
    
    # Read existing .env or create from example
    if os.path.exists(env_path):
        print(f"✅ Found existing .env file")
        with open(env_path, 'r') as f:
            lines = f.readlines()
    elif os.path.exists('.env.example'):
        print(f"📋 Creating .env from .env.example")
        with open('.env.example', 'r') as f:
            lines = f.readlines()
    else:
        print(f"⚠️  No .env or .env.example found, creating new .env")
        lines = []
    
    # Update or add Google Drive settings
    updated_lines = []
    found_folder_id = False
    found_enabled = False
    found_backup = False
    found_creds_path = False
    
    for line in lines:
        if line.startswith('GOOGLE_DRIVE_FOLDER_ID='):
            updated_lines.append(f'GOOGLE_DRIVE_FOLDER_ID={folder_id}\n')
            found_folder_id = True
        elif line.startswith('GOOGLE_DRIVE_ENABLED='):
            updated_lines.append('GOOGLE_DRIVE_ENABLED=true\n')
            found_enabled = True
        elif line.startswith('BACKUP_ENABLED='):
            updated_lines.append('BACKUP_ENABLED=true\n')
            found_backup = True
        elif line.startswith('GOOGLE_DRIVE_CREDENTIALS_PATH='):
            updated_lines.append('GOOGLE_DRIVE_CREDENTIALS_PATH=credentials.json\n')
            found_creds_path = True
        else:
            updated_lines.append(line)
    
    # Add missing settings
    if not found_folder_id:
        updated_lines.append(f'GOOGLE_DRIVE_FOLDER_ID={folder_id}\n')
    if not found_enabled:
        updated_lines.append('GOOGLE_DRIVE_ENABLED=true\n')
    if not found_backup:
        updated_lines.append('BACKUP_ENABLED=true\n')
    if not found_creds_path:
        updated_lines.append('GOOGLE_DRIVE_CREDENTIALS_PATH=credentials.json\n')
    
    # Write back
    with open(env_path, 'w') as f:
        f.writelines(updated_lines)
    
    print(f"✅ Updated {env_path}")
    print("   Settings added:")
    print(f"   - GOOGLE_DRIVE_ENABLED=true")
    print(f"   - GOOGLE_DRIVE_CREDENTIALS_PATH=credentials.json")
    print(f"   - GOOGLE_DRIVE_FOLDER_ID={folder_id}")
    print(f"   - BACKUP_ENABLED=true")


def test_connection():
    """Test Google Drive connection"""
    print_step(4, "Test Connection")
    
    print("Testing Google Drive connection...")
    print("")
    
    try:
        from backend.services.google_drive_service import GoogleDriveService
        
        drive = GoogleDriveService()
        
        if not drive.connected:
            print("❌ Failed to connect to Google Drive")
            print("   Please check your credentials and folder ID")
            return False
        
        print("✅ Successfully connected to Google Drive!")
        
        # Get storage info
        info = drive.get_storage_info()
        print(f"\n📊 Storage Information:")
        print(f"   Total Files:  {info['total_files']}")
        print(f"   Total Size:   {info['total_size_mb']:.2f} MB")
        print(f"   Folder ID:    {info['folder_id']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main setup wizard"""
    print_header("GOOGLE DRIVE SETUP WIZARD")
    print("This wizard will help you set up Google Drive integration for backups.")
    print("")
    
    # Step 1: Check credentials
    has_creds, creds = check_credentials_file()
    if not has_creds:
        print("\n❌ Setup cannot continue without credentials.json")
        print("   Please follow the instructions above to create it.")
        return False
    
    # Show service account email
    print(f"\n📧 Service Account Email: {creds.get('client_email')}")
    print("   ⚠️  Remember to share your Google Drive folder with this email!")
    
    # Step 2: Get folder ID
    folder_id = get_folder_id()
    if not folder_id:
        print("\n❌ Setup cannot continue without folder ID")
        return False
    
    # Step 3: Update .env
    update_env_file(folder_id)
    
    # Step 4: Test connection
    success = test_connection()
    
    # Final summary
    print_header("SETUP COMPLETE!" if success else "SETUP INCOMPLETE")
    
    if success:
        print("✅ Google Drive is fully configured and working!")
        print("")
        print("What happens now:")
        print("  • Database backups will run automatically at 11 PM daily")
        print("  • Reports will be backed up after generation")
        print("  • All backups are stored in your Google Drive folder")
        print("")
        print("Manual backup commands:")
        print("  • Backup database:")
        print("    python -c 'from backend.services.google_drive_service import backup_now; backup_now()'")
        print("")
        print("  • List backups:")
        print("    python -c 'from backend.services.google_drive_service import list_all_backups; print(list_all_backups())'")
        print("")
        print("View all backups at: https://drive.google.com")
    else:
        print("❌ Please fix the errors above and run this wizard again:")
        print("   python setup_google_drive.py")
    
    print("")
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
