import os
from googleapiclient.discovery import build

print("=" * 60)
print("📺 TESTING API KEY FOR YOUTUBE")
print("=" * 60)

api_key = "AIzaSyBtBCH1DyB-pDWxOMj_-Uawr7dJQqfUbc4"

try:
    # Try YouTube API
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    request = youtube.search().list(
        part="snippet",
        q="stock trading",
        type="video",
        maxResults=1
    )
    response = request.execute()
    
    print("\n✅ YouTube API KEY WORKS!")
    print(f"Found {len(response.get('items', []))} results")
    print("\nThis key can be used for YouTube API!")
    
except Exception as e:
    print(f"\n❌ YouTube API Error: {e}")
    print("\nThis key is restricted to Gemini only.")
    print("You need to create a SEPARATE API key for YouTube.")

print("\n" + "=" * 60)
