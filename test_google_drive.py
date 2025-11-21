import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

print("=" * 60)
print("🔍 GOOGLE DRIVE VERIFICATION TEST")
print("=" * 60)

# Check credentials file
creds_path = "credentials.json"
if not os.path.exists(creds_path):
    print("\n❌ credentials.json NOT FOUND")
    exit(1)

print(f"\n✅ Step 1: credentials.json found")

try:
    # Load credentials
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(
        creds_path, scopes=SCOPES
    )
    print("✅ Step 2: Credentials loaded successfully")
    
    # Build Drive service
    service = build('drive', 'v3', credentials=credentials)
    print("✅ Step 3: Google Drive service initialized")
    
    # Test API access - list files
    print("\n🧪 Testing API access...")
    results = service.files().list(pageSize=10).execute()
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! GOOGLE DRIVE API WORKING!")
    print("=" * 60)
    
    print(f"\n📊 Service Account Email: {credentials.service_account_email}")
    print("✅ Authentication: SUCCESSFUL")
    print("✅ API Access: WORKING")
    
    # List accessible files/folders
    items = results.get('files', [])
    print(f"\n📁 Accessible files/folders: {len(items)}")
    
    if items:
        print("\nFiles you can access:")
        for item in items[:5]:
            print(f"  - {item['name']} (ID: {item['id']})")
    else:
        print("\nℹ️  No files accessible yet.")
        print("You need to:")
        print("1. Create a folder in Google Drive")
        print("2. Share it with: gitta-trader-backup@gitta-trader-backup.iam.gserviceaccount.com")
        print("3. Add the folder ID to .env")
    
    print("\n" + "=" * 60)
    
except Exception as e:
    print("\n" + "=" * 60)
    print("❌ ERROR")
    print("=" * 60)
    print(f"\nError: {str(e)}\n")
