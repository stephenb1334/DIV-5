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

def explore_latent_embeddings():
    """
    Explore the actual high-dimensional latent embeddings from Nomic Atlas.
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
        print(f"Sample legal documents:")
        for i in range(min(3, len(df))):
            print(f"  {i}. {df.iloc[i]['category']} - {df.iloc[i]['text'][:80]}...")
        
        # Get the embeddings object
        embeddings_obj = first_map.embeddings
        
        # Try to access the actual high-dimensional latent embeddings
        print(f"\n=== Latent Embeddings (Real Semantic Vectors) ===")
        try:
            latent_embeddings = embeddings_obj.latent
            print(f"Latent embeddings type: {type(latent_embeddings)}")
            
            if hasattr(latent_embeddings, 'shape'):
                print(f"Latent embeddings shape: {latent_embeddings.shape}")
                
            # If it's a DataFrame, explore its structure
            if hasattr(latent_embeddings, 'columns'):
                print(f"Number of latent columns: {len(latent_embeddings.columns)}")
                print(f"First 10 column names: {list(latent_embeddings.columns[:10])}")
                print(f"Latent embeddings head:")
                print(latent_embeddings.head())
                
                # Try to get numeric embeddings for similarity testing
                numeric_latent = latent_embeddings.select_dtypes(include=[np.number])
                if len(numeric_latent.columns) > 0:
                    print(f"\nNumeric latent embedding dimensions: {numeric_latent.shape}")
                    print(f"Sample embedding vector (first 10 dims): {numeric_latent.iloc[0].values[:10]}")
                    
                    # Test semantic similarity with actual embeddings
                    print(f"\n=== Testing Real Semantic Similarity ===")
                    latent_matrix = numeric_latent.values
                    query_latent = latent_matrix[0:1]
                    semantic_similarities = cosine_similarity(query_latent, latent_matrix).flatten()
                    top_semantic_indices = semantic_similarities.argsort()[-4:][::-1][1:]
                    
                    print(f"Query document: {df.iloc[0]['category']} - {df.iloc[0]['text'][:100]}...")
                    print(f"Most semantically similar documents:")
                    for i, idx in enumerate(top_semantic_indices):
                        score = semantic_similarities[idx]
                        print(f"  {i+1}. Score: {score:.4f} - {df.iloc[idx]['category']} - {df.iloc[idx]['text'][:100]}...")
                        
                    return numeric_latent, df  # Return for use in enhanced RAG
                else:
                    print("No numeric columns found in latent embeddings")
            
            # If latent is a numpy array directly
            elif hasattr(latent_embeddings, 'dtype'):
                print(f"Latent embeddings as numpy array shape: {latent_embeddings.shape}")
                print(f"Data type: {latent_embeddings.dtype}")
                if len(latent_embeddings.shape) == 2:
                    print(f"Sample embedding vector: {latent_embeddings[0][:10]}")
                    return latent_embeddings, df
                    
        except Exception as latent_error:
            print(f"Error accessing latent embeddings: {latent_error}")
            import traceback
            traceback.print_exc()
            
        # Also check if we can access embeddings through other methods
        print(f"\n=== Alternative Embedding Access Methods ===")
        
        # Check if there's a way to get embeddings via vector_search input requirements
        print(f"Embeddings object methods: {[method for method in dir(embeddings_obj) if not method.startswith('_')]}")
        
        # Try to understand what vector_search expects
        try:
            print(f"\nTesting vector_search method signature...")
            # This will fail but might give us info about expected format
            fake_query = np.random.rand(1, 512)  # Try common embedding dimensions
            results = embeddings_obj.vector_search(queries=fake_query, k=1)
            print(f"vector_search worked with shape {fake_query.shape}")
        except Exception as vs_error:
            print(f"vector_search error (expected): {vs_error}")
            
        return None, df

    except Exception as e:
        print(f"An error occurred during exploration: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    embeddings, data = explore_latent_embeddings()
    if embeddings is not None:
        print(f"\n✅ SUCCESS: Found {embeddings.shape[1]}-dimensional embeddings for {embeddings.shape[0]} documents!")
    else:
        print(f"\n❌ Could not access high-dimensional embeddings")