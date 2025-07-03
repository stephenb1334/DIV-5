#!/usr/bin/env python3

import openai
import os
from nomic import atlas
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

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

# Atlas project configuration
ATLAS_DATASET_IDENTIFIER = "talon-pro-se/stephen-boerner-divorce-case-data-test-upload"

def generate_response_with_llm(query, retrieved_context):
    """Generate response using OpenRouter LLM."""
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
        {"role": "system", "content": "You are a helpful legal AI assistant specializing in divorce and family law. Answer the user's question based ONLY on the provided case document context. Reference specific documents, dates, and categories when relevant. If the context does not contain enough information, state that clearly. Be precise and cite the source documents."},
        {"role": "user", "content": f"Context from legal case documents:\n\n{context_text}\n\nQuestion: {query}"}
    ]

    try:
        completion = openrouter_client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            stream=False,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred during LLM generation: {e}"

def demo_rag_system():
    print("🏛️  LEGAL RAG SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    try:
        print("📥 Loading dataset...")
        dataset = atlas.AtlasDataset(identifier=ATLAS_DATASET_IDENTIFIER)
        first_map = dataset.maps[0]
        
        print("📊 Loading document data...")
        documents_df = first_map.data.df
        print(f"✅ Loaded {len(documents_df)} legal documents")
        
        # Test queries
        test_queries = [
            "What are the legal theories in my case?",
            "What evidence supports financial abandonment?",
            "Show me financial contribution information"
        ]
        
        for query_num, query in enumerate(test_queries, 1):
            print(f"\n{'='*60}")
            print(f"🔍 TEST QUERY {query_num}: {query}")
            print('='*60)
            
            # Extract text content for search
            texts = documents_df['text'].tolist()
            
            # Create TF-IDF vectors for all texts plus the query
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            all_texts = texts + [query]
            tfidf_matrix = vectorizer.fit_transform(all_texts)
            
            # Calculate similarity between query (last item) and all documents
            query_vector = tfidf_matrix[-1]
            doc_vectors = tfidf_matrix[:-1]
            similarities = cosine_similarity(query_vector, doc_vectors).flatten()
            
            # Get top-3 most similar documents
            top_indices = similarities.argsort()[-3:][::-1]
            
            retrieved_data = []
            print(f"\n📄 TOP 3 RETRIEVED DOCUMENTS:")
            for i, idx in enumerate(top_indices):
                score = similarities[idx]
                if score > 0:  # Only include documents with some similarity
                    row = documents_df.iloc[idx]
                    data_item = {
                        'text': row['text'],
                        'category': row['category'],
                        'date_period': row['date_period'],
                        'source_document': row['source_document'],
                        'legal_theory_supported': row['legal_theory_supported'],
                        'contribution_type': row['contribution_type']
                    }
                    retrieved_data.append(data_item)
                    print(f"  {i+1}. Score: {score:.4f} | {row['category']} | {row['text'][:80]}...")
            
            # Generate AI response
            print(f"\n🤖 GENERATING AI RESPONSE...")
            response = generate_response_with_llm(query, retrieved_data)
            print(f"\n💡 **AI Legal Analysis:**")
            print(f"{response}")
        
        print(f"\n✅ RAG System demonstration completed!")

    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_rag_system()