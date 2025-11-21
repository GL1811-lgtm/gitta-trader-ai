import os
import shutil
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class GoogleDriveArchiver:
    """
    Archives data to Google Drive for 'Infinite Memory'.
    Compresses the data folder and uploads it.
    """

    def __init__(self):
        self.credentials_path = os.getenv("GOOGLE_DRIVE_CREDENTIALS_PATH", "credentials.json")
        self.folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
        self.service = None

    def connect(self) -> bool:
        if not os.path.exists(self.credentials_path):
            print("Google Drive credentials not found.")
            return False
        
        try:
            creds = service_account.Credentials.from_service_account_file(
                self.credentials_path, scopes=['https://www.googleapis.com/auth/drive']
            )
            self.service = build('drive', 'v3', credentials=creds)
            print("Google Drive connected successfully.")
            return True
        except Exception as e:
            print(f"Google Drive connection failed: {e}")
            return False

    def upload_file(self, file_path: str, folder_id: str = None) -> str:
        """Uploads a single file to Drive. Returns File ID."""
        if not self.service:
            if not self.connect():
                return None

        try:
            file_name = os.path.basename(file_path)
            metadata = {'name': file_name}
            if folder_id:
                metadata['parents'] = [folder_id]
            elif self.folder_id:
                metadata['parents'] = [self.folder_id]

            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(body=metadata, media_body=media, fields='id').execute()
            print(f"Uploaded {file_name} (ID: {file.get('id')})")
            return file.get('id')
        except Exception as e:
            print(f"Upload failed for {file_path}: {e}")
            return None

    def create_folder(self, folder_name: str, parent_id: str = None) -> str:
        """Creates a folder in Drive. Returns Folder ID."""
        if not self.service:
            if not self.connect():
                return None

        try:
            metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_id:
                metadata['parents'] = [parent_id]
            elif self.folder_id:
                metadata['parents'] = [self.folder_id]

            file = self.service.files().create(body=metadata, fields='id').execute()
            print(f"Created folder {folder_name} (ID: {file.get('id')})")
            return file.get('id')
        except Exception as e:
            print(f"Folder creation failed: {e}")
            return None

    def archive_data(self, source_dir: str = "backend/data") -> bool:
        """
        Compresses the source directory and uploads to Drive.
        """
        try:
            # 1. Compress
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"gitta_data_archive_{timestamp}"
            shutil.make_archive(archive_name, 'zip', source_dir)
            file_path = f"{archive_name}.zip"

            # 2. Upload
            file_id = self.upload_file(file_path)
            
            # 3. Cleanup
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return file_id is not None

        except Exception as e:
            print(f"Archiving failed: {e}")
            return False
