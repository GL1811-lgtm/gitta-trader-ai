"""
Google Drive Backup Service for Gitta Trader AI
Handles automated backups of database and reports to Google Drive
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io


class GoogleDriveService:
    """Service for managing backups to Google Drive"""
    
    def __init__(self, credentials_path: str = None, folder_id: str = None):
        """
        Initialize Google Drive service
        
        Args:
            credentials_path: Path to service account credentials JSON
            folder_id: Google Drive folder ID for backups
        """
        self.credentials_path = credentials_path or os.getenv(
            'GOOGLE_DRIVE_CREDENTIALS_PATH', 
            'credentials.json'
        )
        self.folder_id = folder_id or os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        self.service = None
        self.connected = False
        
        # Validate configuration
        if not os.path.exists(self.credentials_path):
            print(f"⚠️  Google Drive credentials not found at {self.credentials_path}")
            return
            
        if not self.folder_id:
            print("⚠️  Google Drive folder ID not set in environment")
            return
        
        # Initialize service
        try:
            self._authenticate()
            print("✅ Google Drive service initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Google Drive: {e}")
    
    def _authenticate(self):
        """Authenticate with Google Drive API"""
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        
        # Check for JSON string in environment variable (for cloud deployment)
        creds_json_str = os.getenv('GOOGLE_DRIVE_CREDENTIALS_JSON')
        
        if creds_json_str:
            # Use credentials from environment variable
            try:
                creds_dict = json.loads(creds_json_str)
                credentials = service_account.Credentials.from_service_account_info(
                    creds_dict, 
                    scopes=SCOPES
                )
                print("✅ Loaded Google Drive credentials from environment variable")
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse GOOGLE_DRIVE_CREDENTIALS_JSON: {e}")
                raise
        else:
            # Fall back to credentials file
            if not os.path.exists(self.credentials_path):
                raise FileNotFoundError(f"Credentials file not found at {self.credentials_path}")
            
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path, 
                scopes=SCOPES
            )
            print(f"✅ Loaded Google Drive credentials from file: {self.credentials_path}")
        
        self.service = build('drive', 'v3', credentials=credentials)
        self.connected = True
    
    def backup_database(self, db_path: str = None) -> Optional[str]:
        """
        Backup SQLite database to Google Drive
        
        Args:
            db_path: Path to database file (defaults to backend/data/gitta.db)
            
        Returns:
            File ID of uploaded backup, or None if failed
        """
        if not self.connected:
            print("❌ Google Drive not connected")
            return None
        
        # Default database path
        if not db_path:
            db_path = os.path.join(
                os.path.dirname(__file__), 
                '../../backend/data/gitta.db'
            )
        
        if not os.path.exists(db_path):
            print(f"❌ Database not found at {db_path}")
            return None
        
        try:
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"gitta_db_backup_{timestamp}.db"
            
            # Upload to Google Drive
            file_metadata = {
                'name': backup_name,
                'parents': [self.folder_id]
            }
            
            media = MediaFileUpload(db_path, mimetype='application/x-sqlite3')
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, size'
            ).execute()
            
            file_size_mb = int(file.get('size', 0)) / (1024 * 1024)
            print(f"✅ Database backed up: {backup_name} ({file_size_mb:.2f} MB)")
            print(f"   File ID: {file.get('id')}")
            
            # Clean up old backups (keep last 7 days)
            self._cleanup_old_backups('gitta_db_backup_', max_age_days=7)
            
            return file.get('id')
            
        except Exception as e:
            print(f"❌ Database backup failed: {e}")
            return None
    
    def backup_report(self, report_path: str, report_type: str = "daily") -> Optional[str]:
        """
        Backup a report file to Google Drive
        
        Args:
            report_path: Path to report file
            report_type: Type of report (daily, morning, evening)
            
        Returns:
            File ID of uploaded report, or None if failed
        """
        if not self.connected:
            print("❌ Google Drive not connected")
            return None
        
        if not os.path.exists(report_path):
            print(f"❌ Report not found at {report_path}")
            return None
        
        try:
            # Create formatted filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_name = f"{report_type}_report_{timestamp}.txt"
            
            file_metadata = {
                'name': report_name,
                'parents': [self.folder_id]
            }
            
            media = MediaFileUpload(report_path, mimetype='text/plain')
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name'
            ).execute()
            
            print(f"✅ Report backed up: {report_name}")
            return file.get('id')
            
        except Exception as e:
            print(f"❌ Report backup failed: {e}")
            return None
    
    def upload_file(self, file_path: str, drive_filename: str = None) -> Optional[str]:
        """
        Upload any file to Google Drive
        
        Args:
            file_path: Path to file to upload
            drive_filename: Name for file in Drive (defaults to original name)
            
        Returns:
            File ID of uploaded file, or None if failed
        """
        if not self.connected:
            return None
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None
        
        try:
            filename = drive_filename or os.path.basename(file_path)
            
            file_metadata = {
                'name': filename,
                'parents': [self.folder_id]
            }
            
            media = MediaFileUpload(file_path)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            print(f"✅ Uploaded: {filename}")
            return file.get('id')
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return None
    
    def list_backups(self, prefix: str = "") -> List[Dict]:
        """
        List all backup files in the Drive folder
        
        Args:
            prefix: Filter files by name prefix
            
        Returns:
            List of file metadata dictionaries
        """
        if not self.connected:
            return []
        
        try:
            query = f"'{self.folder_id}' in parents and trashed=false"
            if prefix:
                query += f" and name contains '{prefix}'"
            
            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, size, createdTime, modifiedTime)"
            ).execute()
            
            files = results.get('files', [])
            
            # Sort by creation time (newest first)
            files.sort(key=lambda x: x.get('createdTime', ''), reverse=True)
            
            return files
            
        except Exception as e:
            print(f"❌ Failed to list backups: {e}")
            return []
    
    def download_backup(self, file_id: str, destination_path: str) -> bool:
        """
        Download a backup file from Google Drive
        
        Args:
            file_id: Google Drive file ID
            destination_path: Local path to save file
            
        Returns:
            True if successful, False otherwise
        """
        if not self.connected:
            return False
        
        try:
            request = self.service.files().get_media(fileId=file_id)
            
            with io.FileIO(destination_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    if status:
                        progress = int(status.progress() * 100)
                        print(f"   Download progress: {progress}%", end='\r')
            
            print(f"\n✅ Downloaded to: {destination_path}")
            return True
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def delete_file(self, file_id: str) -> bool:
        """
        Delete a file from Google Drive
        
        Args:
            file_id: Google Drive file ID
            
        Returns:
            True if successful, False otherwise
        """
        if not self.connected:
            return False
        
        try:
            self.service.files().delete(fileId=file_id).execute()
            print(f"✅ Deleted file: {file_id}")
            return True
            
        except Exception as e:
            print(f"❌ Delete failed: {e}")
            return False
    
    def _cleanup_old_backups(self, prefix: str, max_age_days: int = 7):
        """
        Delete backup files older than specified days
        
        Args:
            prefix: Filename prefix to filter
            max_age_days: Maximum age of backups to keep
        """
        try:
            from datetime import timedelta
            
            cutoff_date = datetime.now() - timedelta(days=max_age_days)
            backups = self.list_backups(prefix=prefix)
            
            deleted_count = 0
            for backup in backups:
                created_time = datetime.fromisoformat(
                    backup['createdTime'].replace('Z', '+00:00')
                )
                
                if created_time < cutoff_date.astimezone():
                    self.delete_file(backup['id'])
                    deleted_count += 1
            
            if deleted_count > 0:
                print(f"🗑️  Cleaned up {deleted_count} old backup(s)")
                
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
    
    def get_storage_info(self) -> Dict:
        """
        Get storage usage information
        
        Returns:
            Dictionary with storage stats
        """
        if not self.connected:
            return {}
        
        try:
            backups = self.list_backups()
            total_size = sum(int(f.get('size', 0)) for f in backups)
            
            return {
                'total_files': len(backups),
                'total_size_mb': total_size / (1024 * 1024),
                'total_size_gb': total_size / (1024 * 1024 * 1024),
                'connected': self.connected,
                'folder_id': self.folder_id
            }
            
        except Exception as e:
            print(f"❌ Failed to get storage info: {e}")
            return {}


# Convenience functions for common operations

def backup_now(db_path: str = None) -> bool:
    """Quick backup of database"""
    drive = GoogleDriveService()
    if drive.connected:
        return drive.backup_database(db_path) is not None
    return False


def list_all_backups() -> List[Dict]:
    """List all backups in Drive folder"""
    drive = GoogleDriveService()
    return drive.list_backups()


def restore_latest_backup(destination: str = None) -> bool:
    """Restore the most recent database backup"""
    drive = GoogleDriveService()
    if not drive.connected:
        return False
    
    backups = drive.list_backups(prefix="gitta_db_backup_")
    if not backups:
        print("❌ No backups found")
        return False
    
    latest = backups[0]
    dest_path = destination or "backend/data/gitta_restored.db"
    
    print(f"📥 Restoring backup: {latest['name']}")
    return drive.download_backup(latest['id'], dest_path)


if __name__ == "__main__":
    # Test Google Drive connection
    print("🧪 Testing Google Drive Service...")
    print("-" * 50)
    
    drive = GoogleDriveService()
    
    if drive.connected:
        print("\n📊 Storage Information:")
        info = drive.get_storage_info()
        print(f"   Total files: {info['total_files']}")
        print(f"   Total size: {info['total_size_mb']:.2f} MB")
        print(f"   Folder ID: {info['folder_id']}")
        
        print("\n📋 Recent Backups:")
        backups = drive.list_backups()
        for i, backup in enumerate(backups[:5], 1):
            size_mb = int(backup.get('size', 0)) / (1024 * 1024)
            print(f"   {i}. {backup['name']} ({size_mb:.2f} MB)")
    else:
        print("\n❌ Google Drive not connected")
        print("   Please check credentials and folder ID in .env")
