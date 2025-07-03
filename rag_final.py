import openai
import os
from nomic import atlas
import json
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

# --- Step 1: Retrieval (using Nomic Atlas) ---
def retrieve_relevant_data(query, k=3):
    """
    Retrieves top-k semantically similar data points from Nomic Atlas based on the query.
    """
    print(f"\n--- Step 1: Retrieving relevant data for query: '{query}' ---")
    try:
        # Use AtlasDataset with the correct Nomic 3.0 format
        dataset = atlas.AtlasDataset(identifier=ATLAS_DATASET_IDENTIFIER)
        
        # Get the first (and only) map from the list
        first_map = dataset.maps[0]
        print(f"Using map: {first_map.name} (ID: {first_map.id})")

        # Perform vector search using embeddings - convert query to numpy array
        queries_array = np.array([query])
        results = first_map.embeddings.vector_search(queries=queries_array, k=k)
        
        print(f"Vector search results structure: {type(results)}")
        print(f"Results keys: {list(results.keys()) if isinstance(results, dict) else 'Not a dict'}")
        
        retrieved_data = []
        
        # Handle different possible result structures
        if isinstance(results, dict):
            # Try common result structure patterns
            if 'neighbors' in results and 'distances' in results:
                neighbors = results['neighbors'][0] if isinstance(results['neighbors'][0], (list, np.ndarray)) else results['neighbors']
                distances = results['distances'][0] if isinstance(results['distances'][0], (list, np.ndarray)) else results['distances']
                
                for idx, score in zip(neighbors, distances):
                    # Retrieve the original data point from the local JSON file
                    with open("nomic_atlas_data.json", "r") as f:
                        all_data = json.load(f)
                    
                    if idx < len(all_data):
                        retrieved_data.append(all_data[idx])
                        print(f"  - Retrieved (Score: {score:.4f}): {all_data[idx]['text'][:100]}...")
                    else:
                        print(f"  - Warning: Index {idx} out of bounds for local data.")
            else:
                print(f"Unexpected results structure: {results}")
        else:
            print(f"Results is not a dictionary: {results}")
            
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

    context_text = "\n".join([item['text'] for item in retrieved_context])
    
    messages = [
        {"role": "system", "content": "You are a helpful legal AI assistant. Answer the user's question based ONLY on the provided context. If the context does not contain enough information, state that you cannot answer based on the provided information. Be concise and precise."},
        {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
    ]

    try:
        completion = openrouter_client.chat.completions.create(
            model="auto",  # OpenRouter will auto-select the best available model
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
    user_query = input("Enter your legal question (e.g., 'What evidence supports financial abandonment?'): ")

    # 1. Retrieve relevant data from Nomic Atlas
    context_data = retrieve_relevant_data(user_query, k=5)

    # 2. Augment and 3. Generate response using LLM
    final_response = generate_response_with_llm(user_query, context_data)

    print("\n--- Final RAG System Response ---")
    print(final_response)