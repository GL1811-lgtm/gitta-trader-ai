import os

# Test 1: YouTube API (should work with API key)
print("=" * 60)
print("Test 1: YOUTUBE API")
print("=" * 60)

api_key = "AIzaSyD4bXdU9dVn7R9bKg0wIsOiGvHdMZY7lt4"

try:
    from googleapiclient.discovery import build
    
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        q="stock trading india",
        type="video",
        maxResults=2
    )
    response = request.execute()
    
    print("\n✅ YOUTUBE API WORKS!")
    print(f"Found {len(response.get('items', []))} videos")
    for item in response.get('items', []):
        print(f"  - {item['snippet']['title']}")
    
except Exception as e:
    print(f"\n❌ YouTube Error: {e}")

# Test 2: Google Drive API (won't work with just API key)
print("\n" + "=" * 60)
print("Test 2: GOOGLE DRIVE API")
print("=" * 60)

try:
    # This will fail - Drive needs service account, not API key
    drive = build('drive', 'v3', developerKey=api_key)
    results = drive.files().list(pageSize=5).execute()
    print("\n✅ Drive works (unexpected!)")
    
except Exception as e:
    print("\n❌ Google Drive Error (EXPECTED):")
    print(f"   {str(e)[:100]}...")
    print("\n💡 Why: Google Drive requires SERVICE ACCOUNT credentials,")
    print("   not just an API key. We already have credentials.json.")
    print("   We just need to enable the Drive API and add folder ID!")

print("\n" + "=" * 60)
