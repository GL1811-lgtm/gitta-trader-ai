# This file makes the Flask app discoverable for WSGI servers like Gunicorn.
# It imports the 'app' instance from the main application file.

import sys
import os

# Ensure the backend directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.app import app

# The WSGI server will look for this 'app' object.
