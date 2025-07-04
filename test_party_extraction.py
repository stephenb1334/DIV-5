#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from advanced_hybrid_rag_system import AdvancedHybridRAGSystem
import time

def test_party_queries():
    """Test the enhanced party information extraction"""
    print("🧪 Testing Enhanced Party Information Extraction...")
    
    # Wait for system to initialize
    print("⏳ Waiting for system initialization...")
    time.sleep(5)
    
    try:
        # Initialize system
        system = AdvancedHybridRAGSystem()
        
        if not system.is_initialized:
            print("❌ System not initialized properly")
            return
        
        print("✅ System initialized successfully!")
        
        # Test queries
        test_queries = [
            "Who are the parties of this legal case?",
            "Who is the plaintiff?",
            "Who is the defendant?", 
            "Who is the opposing counsel?",
            "Who are the attorneys in this case?"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing query: '{query}'")
            
            # Test memory search specifically
            memory_results = system._search_memory_graph(query, max_results=5)
            
            print(f"📊 Memory search found {len(memory_results)} results:")
            for i, result in enumerate(memory_results, 1):
                print(f"  {i}. Source: {result.source}")
                print(f"     Category: {result.category}")
                print(f"     Relevance: {result.relevance_score:.3f}")
                print(f"     Entity: {result.metadata.get('entity_name', 'N/A')}")
                print(f"     Type: {result.metadata.get('entity_type', 'N/A')}")
                print(f"     Is Party Info: {result.metadata.get('is_party_info', False)}")
                print(f"     Content Preview: {result.content[:100]}...")
                print()
        
        print("✅ Party extraction testing completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_party_queries()