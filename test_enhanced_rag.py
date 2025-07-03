#!/usr/bin/env python3

import openai
import os
from nomic import atlas
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# --- Configuration ---
NOMIC_API_KEY = "nk-J0k-R6tIByJr-iN9VF2FbGTrgYw_15YxmjVZhWpaZ50"

# --- OpenRouter Configuration ---
OPENROUTER_API_KEY = "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"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Initialize the OpenAI client to use OpenRouter's API
openrouter_client = openai.OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

# Atlas project configuration (Nomic 3.0 format: organization_name/project_name)
ATLAS_DATASET_IDENTIFIER = "talon-pro-se/stephen-boerner-divorce-case-data-test-upload"

print("🔄 Testing Enhanced RAG System (Non-interactive)")
print("=" * 60)

try:
    print("📥 Loading dataset...")
    dataset = atlas.AtlasDataset(identifier=ATLAS_DATASET_IDENTIFIER)
    first_map = dataset.maps[0]
    
    print("📊 Loading document data...")
    documents_df = first_map.data.df
    print(f"✅ Loaded {len(documents_df)} legal documents")
    
    print("🧠 Loading 768-dimensional embeddings...")
    document_embeddings = first_map.embeddings.latent
    print(f"✅ Loaded {document_embeddings.shape[1]}-dimensional embeddings")
    print(f"📊 Embedding matrix shape: {document_embeddings.shape}")
    
    print("🤖 Initializing SentenceTransformer...")
    embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    print("✅ SentenceTransformer ready")
    
    # Test query
    test_query = "What evidence supports financial abandonment?"
    print(f"\n🔍 Testing query: '{test_query}'")
    
    print("🧮 Embedding query...")
    query_embedding = embedding_model.encode([test_query])
    print(f"Query embedding shape: {query_embedding.shape}")
    
    print("📐 Calculating similarities...")
    similarities = cosine_similarity(query_embedding, document_embeddings).flatten()
    print(f"Similarity scores shape: {similarities.shape}")
    
    # Show top 5 similarities
    top_indices = similarities.argsort()[-5:][::-1]
    print(f"\n🏆 Top 5 similarity scores:")
    for i, idx in enumerate(top_indices):
        score = similarities[idx]
        row = documents_df.iloc[idx]
        print(f"  {i+1}. Score: {score:.6f} | {row['category']} | {row['text'][:60]}...")
    
    print(f"\n✅ Enhanced RAG System test completed successfully!")
    print(f"📊 Similarity range: {similarities.min():.6f} to {similarities.max():.6f}")

except Exception as e:
    print(f"❌ Error during test: {e}")
    import traceback
    traceback.print_exc()