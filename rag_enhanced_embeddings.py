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

# Initialize sentence transformer for query embedding (768-dimensional to match Nomic Atlas)
embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

class EnhancedRAGSystem:
    def __init__(self):
        self.document_embeddings = None
        self.documents_df = None
        self.load_data()
    
    def load_data(self):
        """Load document data and pre-computed embeddings from Nomic Atlas."""
        try:
            print("🔄 Loading legal case data and embeddings from Nomic Atlas...")
            
            # Load dataset
            dataset = atlas.AtlasDataset(identifier=ATLAS_DATASET_IDENTIFIER)
            first_map = dataset.maps[0]
            
            # Load document data
            self.documents_df = first_map.data.df
            print(f"✅ Loaded {len(self.documents_df)} legal documents")
            
            # Load high-dimensional embeddings (768-dimensional)
            self.document_embeddings = first_map.embeddings.latent
            print(f"✅ Loaded {self.document_embeddings.shape[1]}-dimensional embeddings")
            print(f"📊 Embedding matrix shape: {self.document_embeddings.shape}")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            import traceback
            traceback.print_exc()
    
    def embed_query(self, query):
        """Embed user query using sentence transformer."""
        try:
            # Use sentence transformer to embed the query
            query_embedding = embedding_model.encode([query])
            return query_embedding
        except Exception as e:
            print(f"❌ Error embedding query: {e}")
            return None
    
    def retrieve_relevant_documents(self, query, k=5):
        """Retrieve top-k most semantically similar documents using TF-IDF fallback."""
        print(f"\n🔍 Retrieving relevant documents for: '{query}'")
        print("⚠️  Note: Using TF-IDF fallback due to embedding compatibility issues")
        
        if self.documents_df is None:
            print("❌ Data not loaded properly")
            return []
        
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            
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
            for i, idx in enumerate(top_indices):
                score = similarities[idx]
                if score > 0:  # Only include documents with some similarity
                    row = self.documents_df.iloc[idx]
                    doc_info = {
                        'index': idx,
                        'similarity_score': score,
                        'category': row['category'],
                        'date_period': row['date_period'],
                        'source_document': row['source_document'],
                        'legal_theory_supported': row['legal_theory_supported'],
                        'contribution_type': row['contribution_type'],
                        'text': row['text']
                    }
                    retrieved_docs.append(doc_info)
                    print(f"  📄 Doc {i+1}: Score={score:.4f} | {row['category']} | {row['text'][:80]}...")
            
            if not retrieved_docs:
                print("⚠️  No documents found with similarity > 0")
                    
            return retrieved_docs
            
        except Exception as e:
            print(f"❌ Error during retrieval: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def generate_response(self, query, retrieved_docs):
        """Generate AI response using retrieved documents as context."""
        print(f"\n🤖 Generating AI response...")
        
        if not retrieved_docs:
            return "I couldn't find relevant information in your case documents to answer that question."
        
        # Format context with rich metadata
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            context_part = f"Document {i} (Similarity: {doc['similarity_score']:.3f}):\n"
            context_part += f"  Category: {doc['category']}\n"
            context_part += f"  Date: {doc['date_period']}\n"
            context_part += f"  Source: {doc['source_document']}\n"
            context_part += f"  Legal Theory: {doc['legal_theory_supported']}\n"
            context_part += f"  Content: {doc['text']}\n"
            context_parts.append(context_part)
        
        context_text = "\n" + "="*50 + "\n".join(context_parts)
        
        messages = [
            {
                "role": "system", 
                "content": "You are an expert legal AI assistant specializing in divorce and family law. Analyze the provided case documents and answer the user's question with precision. Reference specific documents, similarity scores, dates, and legal theories when relevant. If the context doesn't contain sufficient information, state that clearly. Be thorough but concise."
            },
            {
                "role": "user", 
                "content": f"Legal Case Context:\n{context_text}\n\nQuestion: {query}\n\nPlease provide a detailed analysis based on the most relevant documents."
            }
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
            return f"❌ Error generating response: {e}"
    
    def query(self, user_question, k=5):
        """Main method to perform RAG query."""
        print(f"\n" + "="*60)
        print(f"🏛️  ENHANCED LEGAL RAG SYSTEM")
        print(f"="*60)
        
        # Step 1: Retrieve relevant documents using semantic embeddings
        relevant_docs = self.retrieve_relevant_documents(user_question, k=k)
        
        # Step 2: Generate response using LLM
        response = self.generate_response(user_question, relevant_docs)
        
        print(f"\n💡 **AI Legal Analysis:**")
        print(f"{response}")
        
        return response

# --- Main Execution ---
if __name__ == "__main__":
    # Initialize the enhanced RAG system
    rag_system = EnhancedRAGSystem()
    
    if rag_system.document_embeddings is not None:
        print(f"\n✅ Enhanced RAG System Ready!")
        print(f"📊 {rag_system.document_embeddings.shape[0]} documents with {rag_system.document_embeddings.shape[1]}-dimensional embeddings")
        
        # Interactive query
        user_query = input("\n❓ Enter your legal question: ")
        rag_system.query(user_query, k=5)
    else:
        print("❌ Failed to initialize RAG system")