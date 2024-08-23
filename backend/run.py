# backend/run.py

import os
import sys

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from backend.app import app

if __name__ == "__main__":
    app.run(debug=True)