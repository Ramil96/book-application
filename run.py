import os
from taskmanager import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

if __name__ == "__main__":
    # Default to IP and PORT environment variables if available, otherwise use localhost and a free port.
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),  # Default to "0.0.0.0" if IP is not set
        port=int(os.environ.get("PORT", 5000)),  # Default to port 5000 if PORT is not set
        debug=os.environ.get("DEBUG", "False").lower() == "true"  # Enable debug if DEBUG is "True"
    )
