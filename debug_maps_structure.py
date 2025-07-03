import openai
import os
from nomic import atlas
import json

# --- Configuration ---
NOMIC_API_KEY = "nk-J0k-R6tIByJr-iN9VF2FbGTrgYw_15YxmjVZhWpaZ50"

# Atlas project configuration (Nomic 3.0 format: organization_name/project_name)
ATLAS_DATASET_IDENTIFIER = "talon-pro-se/stephen-boerner-divorce-case-data-test-upload"
ATLAS_MAP_ID = "0197c9a8-2dc7-f538-1298-06c2dae141f8"

def debug_maps_structure():
    """
    Debug script to understand the structure of dataset.maps.
    """
    try:
        # Use AtlasDataset with the correct Nomic 3.0 format
        dataset = atlas.AtlasDataset(identifier=ATLAS_DATASET_IDENTIFIER)
        
        print("=== DEBUG: Dataset Maps Structure ===")
        print(f"Type of dataset.maps: {type(dataset.maps)}")
        
        if hasattr(dataset.maps, '__len__'):
            print(f"Length of dataset.maps: {len(dataset.maps)}")
        
        # If it's a list, let's see what's in it
        if isinstance(dataset.maps, list):
            print(f"dataset.maps is a list with {len(dataset.maps)} items")
            for i, map_item in enumerate(dataset.maps):
                print(f"\nMap {i}:")
                print(f"  Type: {type(map_item)}")
                print(f"  Dir: {[attr for attr in dir(map_item) if not attr.startswith('_')]}")
                
                # Try to get map ID or identifier
                if hasattr(map_item, 'id'):
                    print(f"  ID: {map_item.id}")
                if hasattr(map_item, 'map_id'):
                    print(f"  Map ID: {map_item.map_id}")
                if hasattr(map_item, 'identifier'):
                    print(f"  Identifier: {map_item.identifier}")
                if hasattr(map_item, '__dict__'):
                    print(f"  Attributes: {list(map_item.__dict__.keys())}")
        
        # Let's also try different ways to access maps
        print("\n=== Trying different access methods ===")
        
        # Try accessing the first map if it exists
        if len(dataset.maps) > 0:
            first_map = dataset.maps[0]
            print(f"First map type: {type(first_map)}")
            print(f"First map methods: {[method for method in dir(first_map) if not method.startswith('_')]}")
            
            # Check if this map has vector_search method
            if hasattr(first_map, 'vector_search'):
                print("✓ First map has vector_search method!")
                
                # Try a simple vector search
                try:
                    query = "financial abandonment"
                    results = first_map.vector_search(queries=[query], k=2)
                    print(f"Vector search successful! Results type: {type(results)}")
                    print(f"Results structure: {results}")
                except Exception as search_error:
                    print(f"Vector search failed: {search_error}")
            else:
                print("✗ First map does not have vector_search method")

    except Exception as e:
        print(f"An error occurred during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_maps_structure()