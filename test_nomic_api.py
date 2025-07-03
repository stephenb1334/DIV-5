from nomic import atlas
import json

# Print available methods in atlas module
print("Available methods in nomic.atlas:")
methods = [method for method in dir(atlas) if not method.startswith('_')]
for method in methods:
    print(f"  - {method}")

print("\n" + "="*50)

# Try to access the existing project using the map ID
ATLAS_MAP_ID = "0197c9a8-2dc7-f538-1298-06c2dae141f8"
NOMIC_API_KEY = "nk-J0k-R6tIByJr-iN9VF2FbGTrgYw_15YxmjVZhWpaZ50"

print(f"Attempting to access map with ID: {ATLAS_MAP_ID}")

try:
    # Try different approaches to access the existing map
    
    # Method 1: Try atlas.get_map() if it exists
    if hasattr(atlas, 'get_map'):
        print("Trying atlas.get_map()...")
        map_obj = atlas.get_map(ATLAS_MAP_ID)
        print(f"Success with get_map: {map_obj}")
    
    # Method 2: Try using the map ID directly in some other way
    print("Checking other available methods...")
    
except Exception as e:
    print(f"Error: {e}")