import openai
import os
from nomic import atlas
import json

# --- Configuration ---
NOMIC_API_KEY = "nk-J0k-R6tIByJr-iN9VF2FbGTrgYw_15YxmjVZhWpaZ50"

# Atlas project configuration (Nomic 3.0 format: organization_name/project_name)
ATLAS_DATASET_IDENTIFIER = "talon-pro-se/stephen-boerner-divorce-case-data-test-upload"

def debug_embeddings():
    """
    Debug script to understand how to perform vector search using embeddings.
    """
    try:
        # Use AtlasDataset with the correct Nomic 3.0 format
        dataset = atlas.AtlasDataset(identifier=ATLAS_DATASET_IDENTIFIER)
        
        # Get the first (and only) map
        first_map = dataset.maps[0]
        print(f"=== DEBUG: Map Information ===")
        print(f"Map ID: {first_map.id}")
        print(f"Map Name: {first_map.name}")
        print(f"Map Type: {type(first_map)}")
        
        # Explore the embeddings property
        print(f"\n=== DEBUG: Embeddings ===")
        embeddings = first_map.embeddings
        print(f"Embeddings type: {type(embeddings)}")
        print(f"Embeddings methods: {[method for method in dir(embeddings) if not method.startswith('_')]}")
        
        # Check if embeddings has vector_search or similar methods
        if hasattr(embeddings, 'vector_search'):
            print("✓ embeddings has vector_search method!")
            
            # Try a vector search
            try:
                query = "financial abandonment"
                results = embeddings.vector_search(queries=[query], k=3)
                print(f"Vector search successful! Results: {results}")
            except Exception as search_error:
                print(f"Vector search failed: {search_error}")
        
        elif hasattr(embeddings, 'search'):
            print("✓ embeddings has search method!")
            
            # Try a search
            try:
                query = "financial abandonment"
                results = embeddings.search(query=query, k=3)
                print(f"Search successful! Results: {results}")
            except Exception as search_error:
                print(f"Search failed: {search_error}")
        
        elif hasattr(embeddings, 'query'):
            print("✓ embeddings has query method!")
            
            # Try a query
            try:
                query = "financial abandonment"
                results = embeddings.query(query=query, k=3)
                print(f"Query successful! Results: {results}")
            except Exception as query_error:
                print(f"Query failed: {query_error}")
        
        else:
            print("✗ No obvious search method found in embeddings")
            
        # Let's also check the dataset itself for search methods
        print(f"\n=== DEBUG: Dataset Methods ===")
        print(f"Dataset methods: {[method for method in dir(dataset) if not method.startswith('_')]}")
        
        # Check if dataset has search functionality
        if hasattr(dataset, 'vector_search'):
            print("✓ dataset has vector_search method!")
            
            # Try dataset vector search
            try:
                query = "financial abandonment"
                results = dataset.vector_search(query=query, k=3)
                print(f"Dataset vector search successful! Results: {results}")
            except Exception as search_error:
                print(f"Dataset vector search failed: {search_error}")

    except Exception as e:
        print(f"An error occurred during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_embeddings()