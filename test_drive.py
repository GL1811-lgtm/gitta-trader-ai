import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.archiver.google_drive import GoogleDriveArchiver

def test_drive_upload():
    print("--- Testing Google Drive Integration ---")
    
    archiver = GoogleDriveArchiver()
    
    # 1. Test Connection
    print("\n1. Testing Connection...")
    if not archiver.connect():
        print("⚠️ Connection failed (Expected if no credentials.json found)")
        print("Skipping upload test.")
        return

    # 2. Test Upload
    print("\n2. Testing File Upload...")
    test_file = "test_upload.txt"
    with open(test_file, "w") as f:
        f.write("This is a test upload from Gitta Trader AI.")
    
    try:
        file_id = archiver.upload_file(test_file)
        if file_id:
            print(f"✅ Upload Successful! File ID: {file_id}")
        else:
            print("❌ Upload Failed.")
    except Exception as e:
        print(f"❌ Error during upload: {e}")
    finally:
        # Cleanup local test file
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    test_drive_upload()
