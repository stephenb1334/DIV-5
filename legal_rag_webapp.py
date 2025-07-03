#!/usr/bin/env python3

import openai
import os
from nomic import atlas
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, render_template, request, jsonify
import traceback
from datetime import datetime

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

# Initialize Flask app
app = Flask(__name__)

class LegalRAGSystem:
    def __init__(self):
        self.documents_df = None
        self.load_data()
    
    def load_data(self):
        """Load document data from Nomic Atlas."""
        try:
            print("🔄 Loading legal case data from Nomic Atlas...")
            dataset = atlas.AtlasDataset(identifier=ATLAS_DATASET_IDENTIFIER)
            first_map = dataset.maps[0]
            self.documents_df = first_map.data.df
            print(f"✅ Loaded {len(self.documents_df)} legal documents")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def retrieve_relevant_documents(self, query, k=5):
        """Retrieve top-k most semantically similar documents using TF-IDF."""
        if self.documents_df is None:
            return []
        
        try:
            # Extract text content for search
            texts = self.documents_df['text'].tolist()
            
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
            
            retrieved_docs = []
            for idx in top_indices:
                score = similarities[idx]
                if score > 0:  # Only include documents with some similarity
                    row = self.documents_df.iloc[idx]
                    doc_info = {
                        'index': int(idx),
                        'similarity_score': float(score),
                        'category': str(row['category']),
                        'date_period': str(row['date_period']),
                        'source_document': str(row['source_document']),
                        'legal_theory_supported': str(row['legal_theory_supported']),
                        'contribution_type': str(row['contribution_type']),
                        'text': str(row['text'])
                    }
                    retrieved_docs.append(doc_info)
            
            return retrieved_docs
            
        except Exception as e:
            print(f"❌ Error during retrieval: {e}")
            traceback.print_exc()
            return []
    
    def generate_response(self, query, retrieved_docs):
        """Generate AI response using retrieved documents as context."""
        if not retrieved_docs:
            return "I couldn't find relevant information in your case documents to answer that question."

        # Format context with metadata
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            context_part = f"Document {i}:\n"
            context_part += f"Category: {doc['category']}\n"
            context_part += f"Date: {doc['date_period']}\n"
            context_part += f"Source: {doc['source_document']}\n"
            context_part += f"Legal Theory: {doc['legal_theory_supported']}\n"
            context_part += f"Content: {doc['text']}\n"
            context_parts.append(context_part)
        
        context_text = "\n---\n".join(context_parts)
        
        messages = [
            {"role": "system", "content": "You are an expert legal AI assistant specializing in divorce and family law. Answer the user's question based ONLY on the provided case document context. Reference specific documents, dates, and categories when relevant. If the context does not contain enough information, state that clearly. Be precise and cite the source documents."},
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
            return f"An error occurred during AI response generation: {e}"
    
    def query(self, user_question, k=5):
        """Main method to perform RAG query."""
        # Step 1: Retrieve relevant documents
        relevant_docs = self.retrieve_relevant_documents(user_question, k=k)
        
        # Step 2: Generate response using LLM
        response = self.generate_response(user_question, relevant_docs)
        
        return {
            'query': user_question,
            'retrieved_documents': relevant_docs,
            'ai_response': response,
            'timestamp': datetime.now().isoformat()
        }

# Initialize the RAG system
rag_system = LegalRAGSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def handle_query():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        # Perform RAG query
        result = rag_system.query(query, k=5)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'documents_loaded': len(rag_system.documents_df) if rag_system.documents_df is not None else 0,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    if rag_system.documents_df is not None:
        print(f"🚀 Legal RAG Web Application Starting...")
        print(f"📊 Loaded {len(rag_system.documents_df)} legal documents")
        print(f"🌐 Access the app at: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5001)
    else:
        print("❌ Failed to load legal documents. Cannot start web application.")