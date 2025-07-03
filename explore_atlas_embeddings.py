import openai
import os
from nomic import atlas
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# --- Configuration ---
NOMIC_API_KEY = "nk-J0k-R6tIByJr-iN9VF2FbGTrgYw_15YxmjVZhWpaZ50"

# Atlas project configuration (Nomic 3.0 format: organization_name/project_name)
ATLAS_DATASET_IDENTIFIER = "talon-pro-se/stephen-boerner-divorce-case-data-test-upload"

def explore_atlas_embeddings():
    """
    Explore the pre-computed embeddings from Nomic Atlas to understand their structure.
    """
    try:
        # Use AtlasDataset to get the actual data
        dataset = atlas.AtlasDataset(identifier=ATLAS_DATASET_IDENTIFIER)
        
        # Get the first (and only) map
        first_map = dataset.maps[0]
        print(f"Using map: {first_map.name} (ID: {first_map.id})")

        # Get the actual data
        df = first_map.data.df
        print(f"\n=== Data Structure ===")
        print(f"Data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Sample data:")
        print(df[['category', 'date_period', 'source_document']].head())
        
        # Get the projected embeddings
        print(f"\n=== Embeddings Structure ===")
        embeddings_obj = first_map.embeddings
        projected_embeddings = embeddings_obj.projected
        
        print(f"Projected embeddings type: {type(projected_embeddings)}")
        print(f"Projected embeddings shape: {projected_embeddings.shape}")
        print(f"Projected embeddings columns: {list(projected_embeddings.columns)}")
        print(f"First few embedding dimensions:")
        print(projected_embeddings.head())
        
        # Check if the number of rows matches our data
        print(f"\nData rows: {len(df)}")
        print(f"Embedding rows: {len(projected_embeddings)}")
        print(f"Match: {len(df) == len(projected_embeddings)}")
        
        # The projected embeddings are just 2D coordinates for visualization
        print(f"\nProjected embeddings are 2D visualization coordinates, not semantic vectors!")
        print(f"We need the actual high-dimensional latent embeddings for semantic search.")
        
        # Extract only the numeric x,y coordinates for testing
        numeric_coords = projected_embeddings[['x', 'y']].values
        print(f"2D coordinates shape: {numeric_coords.shape}")
        
        # Test similarity with the 2D coordinates (just for demonstration)
        print(f"\n=== Testing 2D Coordinate Similarity (Limited Usefulness) ===")
        query_coords = numeric_coords[0:1]  # First document coordinates
        coord_similarities = cosine_similarity(query_coords, numeric_coords).flatten()
        top_coord_indices = coord_similarities.argsort()[-4:][::-1][1:]  # Exclude self
        
        print(f"Query document (index 0): {df.iloc[0]['category']} - {df.iloc[0]['text'][:100]}...")
        print(f"Most similar by 2D coordinates:")
        for i, idx in enumerate(top_coord_indices):
            score = coord_similarities[idx]
            print(f"  {i+1}. Score: {score:.4f} - {df.iloc[idx]['category']} - {df.iloc[idx]['text'][:100]}...")
        
        # Try to access latent embeddings too
        print(f"\n=== Latent Embeddings ===")
        try:
            latent_embeddings = embeddings_obj.latent
            print(f"Latent embeddings type: {type(latent_embeddings)}")
            if hasattr(latent_embeddings, 'shape'):
                print(f"Latent embeddings shape: {latent_embeddings.shape}")
        except Exception as latent_error:
            print(f"Error accessing latent embeddings: {latent_error}")
            
        # Check if we can access the raw embeddings that vector_search expects
        print(f"\n=== Vector Search Requirements ===")
        print(f"Available embeddings methods: {[method for method in dir(embeddings_obj) if not method.startswith('_')]}")

    except Exception as e:
        print(f"An error occurred during exploration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    explore_atlas_embeddings()