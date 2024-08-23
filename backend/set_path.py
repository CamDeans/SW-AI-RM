# backend/set_path.py

import os
import sys

# Get the absolute path of the current file
current_path = os.path.abspath(__file__)

# Get the parent directory of the 'backend' folder
parent_dir = os.path.dirname(os.path.dirname(current_path))

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

# Print the updated sys.path
print("Updated sys.path:")
for path in sys.path:
    print(path)