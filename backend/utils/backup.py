import shutil
import os
import datetime
import logging

logger = logging.getLogger(__name__)

def backup_database(db_path="backend/data/gitta.db", backup_dir="backend/data/backups"):
    """Creates a timestamped copy of the SQLite database."""
    try:
        if not os.path.exists(db_path):
            logger.warning(f"Database not found at {db_path}. Skipping backup.")
            return False

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"gitta_db_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)

        shutil.copy2(db_path, backup_path)
        logger.info(f"Database backed up successfully to {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Database backup failed: {e}")
        return False
