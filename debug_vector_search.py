import openai
import os
from nomic import atlas
import json

# --- Configuration ---
NOMIC_API_KEY = "nk-J0k-R6tIByJr-iN9VF2FbGTrgYw_15YxmjVZhWpaZ50"

# Atlas project configuration (Nomic 3.0 format: organization_name/project_name)
ATLAS_DATASET_IDENTIFIER = "talon-pro-se/stephen-boerner-divorce-case-data-test-upload"
ATLAS_MAP_ID = "0197c9a8-2dc7-f538-1298-06c2dae141f8"

def debug_vector_search():
    """
    Debug script to understand the structure of vector search results.
    """
    try:
        # Use AtlasDataset with the correct Nomic 3.0 format
        dataset = atlas.AtlasDataset(identifier=ATLAS_DATASET_IDENTIFIER)
        
        # Get the map object directly using the map ID
        map_obj = dataset.maps[ATLAS_MAP_ID]

        # Perform vector search
        query = "What evidence supports financial abandonment"
        results = map_obj.vector_search(queries=[query], k=3)
        
        print("=== DEBUG: Vector Search Results Structure ===")
        print(f"Type of results: {type(results)}")
        print(f"Results keys: {list(results.keys()) if isinstance(results, dict) else 'Not a dict'}")
        print(f"Full results structure:")
        print(json.dumps(results, indent=2, default=str))
        
        # Try to understand the structure
        if isinstance(results, dict):
            for key, value in results.items():
                print(f"\nKey: {key}")
                print(f"  Type: {type(value)}")
                if isinstance(value, list) and len(value) > 0:
                    print(f"  Length: {len(value)}")
                    print(f"  First element type: {type(value[0])}")
                    print(f"  First element: {value[0]}")

    except Exception as e:
        print(f"An error occurred during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_vector_search()