import logging
import os
import sys
from logging.handlers import RotatingFileHandler
try:
    from pythonjsonlogger import jsonlogger
    JSON_LOGGING = True
except ImportError:
    JSON_LOGGING = False

def setup_logger(name, log_file='backend.log', level=logging.INFO):
    """Function to setup as many loggers as you want"""
    
    # Ensure logs directory exists
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_path = os.path.join(log_dir, log_file)

    if JSON_LOGGING:
        formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Rotating File Handler: 10MB size, keep 5 backups
    handler = RotatingFileHandler(log_path, maxBytes=10*1024*1024, backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding multiple handlers if logger already exists
    if not logger.handlers:
        logger.addHandler(handler)
        
        # Also log to console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Create a default logger
logger = setup_logger('gitta_trader')
