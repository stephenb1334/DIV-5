#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_memory_interface import MCPMemoryInterface

def test_memory_party_info():
    """Test the MCP Memory party information directly"""
    print("🧪 Testing MCP Memory Party Information...")
    
    try:
        # Initialize MCP Memory directly
        mcp = MCPMemoryInterface()
        
        print("✅ MCP Memory initialized successfully!")
        print(f"📊 Knowledge Summary: {mcp.get_knowledge_summary()}")
        
        # Test party-related queries
        test_queries = [
            "parties",
            "plaintiff", 
            "defendant",
            "attorney",
            "counsel",
            "Helen",
            "Melissa",
            "Stephen",
            "Lafferty"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing query: '{query}'")
            
            # Search entities
            entities = mcp.search_entities(query)
            
            print(f"📊 Found {len(entities)} entities:")
            for i, entity in enumerate(entities, 1):
                print(f"  {i}. {entity.name} ({entity.entity_type})")
                print(f"     Confidence: {entity.confidence_score}")
                print(f"     Observations: {len(entity.observations)}")
                for obs in entity.observations[:2]:  # Show first 2 observations
                    print(f"       • {obs}")
                if len(entity.observations) > 2:
                    print(f"       • ... and {len(entity.observations) - 2} more")
                print()
        
        # Test specific party type searches
        print("\n🎯 Testing specific entity type searches:")
        party_types = ['Plaintiff', 'Defendant', 'OpposingCounsel']
        
        for entity_type in party_types:
            entities = mcp.search_entities("", entity_type=entity_type)
            print(f"\n{entity_type} entities: {len(entities)}")
            for entity in entities:
                print(f"  • {entity.name}: {entity.observations[0] if entity.observations else 'No observations'}")
        
        print("\n✅ MCP Memory party testing completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_memory_party_info()