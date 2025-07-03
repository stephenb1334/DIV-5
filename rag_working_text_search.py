import openai
import os
from nomic import atlas
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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

# --- Step 1: Retrieval (using text-based search) ---
def retrieve_relevant_data(query, k=3):
    """
    Retrieves top-k semantically similar data points using TF-IDF text similarity.
    """
    print(f"\n--- Step 1: Retrieving relevant data for query: '{query}' ---")
    try:
        # Use AtlasDataset to get the actual data
        dataset = atlas.AtlasDataset(identifier=ATLAS_DATASET_IDENTIFIER)
        
        # Get the first (and only) map
        first_map = dataset.maps[0]
        print(f"Using map: {first_map.name} (ID: {first_map.id})")

        # Get the data as a DataFrame
        df = first_map.data.df
        print(f"Data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Extract text content for search
        texts = df['text'].tolist()
        
        # Create TF-IDF vectors for all texts plus the query
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        all_texts = texts + [query]
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Calculate similarity between query (last item) and all documents
        query_vector = tfidf_matrix[-1]
        doc_vectors = tfidf_matrix[:-1]
        similarities = cosine_similarity(query_vector, doc_vectors).flatten()
        
        # Get top-k most similar documents
        top_indices = similarities.argsort()[-k:][::-1]
        
        retrieved_data = []
        for idx in top_indices:
            score = similarities[idx]
            if score > 0:  # Only include documents with some similarity
                row = df.iloc[idx]
                data_item = {
                    'text': row['text'],
                    'category': row['category'],
                    'date_period': row['date_period'],
                    'source_document': row['source_document'],
                    'legal_theory_supported': row['legal_theory_supported'],
                    'contribution_type': row['contribution_type']
                }
                retrieved_data.append(data_item)
                print(f"  - Retrieved (Score: {score:.4f}): {row['category']} - {row['text'][:100]}...")
        
        if not retrieved_data:
            print("  - No relevant documents found with similarity > 0")
            
        return retrieved_data

    except Exception as e:
        print(f"An error occurred during retrieval: {e}")
        import traceback
        traceback.print_exc()
        return []

# --- Step 2 & 3: Augmentation and Generation (using OpenRouter LLM) ---
def generate_response_with_llm(query, retrieved_context):
    """
    Generates a response using an OpenRouter LLM, augmented by the retrieved context.
    """
    print("\n--- Step 2 & 3: Augmenting and Generating Response ---")
    if not retrieved_context:
        return "I couldn't find relevant information in your case data to answer that question."

    # Format context with metadata
    context_parts = []
    for i, item in enumerate(retrieved_context, 1):
        context_part = f"Document {i}:\n"
        context_part += f"Category: {item['category']}\n"
        context_part += f"Date: {item['date_period']}\n"
        context_part += f"Source: {item['source_document']}\n"
        context_part += f"Legal Theory: {item['legal_theory_supported']}\n"
        context_part += f"Content: {item['text']}\n"
        context_parts.append(context_part)
    
    context_text = "\n---\n".join(context_parts)
    
    messages = [
        {"role": "system", "content": "You are a helpful legal AI assistant. Answer the user's question based ONLY on the provided case document context. Reference specific documents, dates, and categories when relevant. If the context does not contain enough information, state that clearly. Be precise and cite the source documents."},
        {"role": "user", "content": f"Context from legal case documents:\n\n{context_text}\n\nQuestion: {query}"}
    ]

    try:
        completion = openrouter_client.chat.completions.create(
            model="openai/gpt-4o-mini",  # Fast, cost-effective model that works well for legal analysis
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            stream=False,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred during LLM generation: {e}"

# --- Main RAG Workflow ---
if __name__ == "__main__":
    print("=== Legal Case RAG System ===")
    print("This system searches your case documents and provides AI-generated responses.")
    print()
    
    user_query = input("Enter your legal question (e.g., 'What evidence supports financial abandonment?'): ")

    # 1. Retrieve relevant data using text similarity
    context_data = retrieve_relevant_data(user_query, k=5)

    # 2. Augment and 3. Generate response using LLM
    final_response = generate_response_with_llm(user_query, context_data)

    print("\n--- Final RAG System Response ---")
    print(final_response)