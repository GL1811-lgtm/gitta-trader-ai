# This file makes the Flask app discoverable for WSGI servers like Gunicorn.
# It imports the 'app' instance from the main application file.

from app import app

# The WSGI server will look for this 'app' object.
