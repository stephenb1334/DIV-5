import json
import os
from nomic import atlas

# Load the data from the generated JSON file
with open("nomic_atlas_data.json", "r") as f:
    nomic_data = json.load(f)

# Ensure your NOMIC_API_KEY is set as an environment variable
# You can set it in your terminal like this:
# export NOMIC_API_KEY="YOUR_API_KEY_HERE"
# Or in your .bashrc, .zshrc, etc.
# For this test upload, we are directly using the provided API key.
# In a production environment, it is highly recommended to use environment variables
# or a secure secret management system for API keys.
nomic_api_key = "nk-J0k-R6tIByJr-iN9VF2FbGTrgYw_15YxmjVZhWpaZ50"

# Initialize Nomic Atlas with your API key

# Upload to Atlas
print(f"Attempting to upload {len(nomic_data)} data points to Nomic Atlas...")
try:
    project = atlas.map_data(
        data=nomic_data,
        indexed_field="text",
        identifier="Stephen Boerner Divorce Case Data - Test Upload",
    )
    print(f"Atlas project created: {project.maps[0].map_link}")
    print("Please visit the link above to view your data in Nomic Atlas.")
except Exception as e:
    print(f"An error occurred during upload: {e}")
