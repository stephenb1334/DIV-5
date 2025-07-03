import openai
import os
from nomic import atlas
import json
import numpy as np

# --- Configuration ---
NOMIC_API_KEY = "nk-J0k-R6tIByJr-iN9VF2FbGTrgYw_15YxmjVZhWpaZ50"

# Atlas project configuration (Nomic 3.0 format: organization_name/project_name)
ATLAS_DATASET_IDENTIFIER = "talon-pro-se/stephen-boerner-divorce-case-data-test-upload"

def debug_text_search():
    """
    Debug script to find text-based search methods or embedding conversion.
    """
    try:
        # Use AtlasDataset with the correct Nomic 3.0 format
        dataset = atlas.AtlasDataset(identifier=ATLAS_DATASET_IDENTIFIER)
        
        # Get the first (and only) map
        first_map = dataset.maps[0]
        print(f"=== DEBUG: Exploring Text Search Options ===")
        
        # Explore all dataset methods for anything search-related
        print(f"\nDataset methods containing 'search':")
        search_methods = [method for method in dir(dataset) if 'search' in method.lower()]
        for method in search_methods:
            print(f"  - {method}")
        
        # Explore all map methods for anything search-related  
        print(f"\nMap methods containing 'search' or 'query':")
        map_search_methods = [method for method in dir(first_map) if 'search' in method.lower() or 'query' in method.lower()]
        for method in map_search_methods:
            print(f"  - {method}")
        
        # Check if we can embed text using the dataset or Atlas
        print(f"\nMethods containing 'embed':")
        embed_methods = [method for method in dir(dataset) if 'embed' in method.lower()]
        for method in embed_methods:
            print(f"  - dataset.{method}")
            
        atlas_embed_methods = [method for method in dir(atlas) if 'embed' in method.lower()]
        for method in atlas_embed_methods:
            print(f"  - atlas.{method}")
        
        # Check embeddings object methods more thoroughly
        embeddings = first_map.embeddings
        print(f"\nAll embeddings methods:")
        for method in dir(embeddings):
            if not method.startswith('_'):
                print(f"  - embeddings.{method}")
                
        # Try to understand the data structure - maybe we can search by text fields
        print(f"\n=== Exploring Data Structure ===")
        
        # Try to get some data to understand format
        if hasattr(first_map, 'data'):
            print(f"Map has data attribute: {type(first_map.data)}")
            if hasattr(first_map.data, 'df'):
                print("Trying to access data.df...")
                try:
                    df = first_map.data.df
                    print(f"Data frame shape: {df.shape}")
                    print(f"Data frame columns: {list(df.columns)}")
                    print(f"First few rows:\n{df.head()}")
                except Exception as df_error:
                    print(f"Error accessing df: {df_error}")
        
        # Try the projected embeddings to see if they give us search capabilities
        if hasattr(embeddings, 'projected'):
            print(f"\nEmbeddings.projected type: {type(embeddings.projected)}")
            projected = embeddings.projected
            
            # Check if projected has search methods
            proj_methods = [method for method in dir(projected) if not method.startswith('_')]
            print(f"Projected methods: {proj_methods}")

    except Exception as e:
        print(f"An error occurred during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_text_search()