#!/usr/bin/env python3

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LegalEntity:
    """Represents a legal entity in the knowledge graph"""
    name: str
    entity_type: str
    observations: List[str]
    metadata: Optional[Dict] = None
    confidence_score: Optional[float] = None
    last_updated: Optional[str] = None

@dataclass
class LegalRelation:
    """Represents a relationship between legal entities"""
    from_entity: str
    to_entity: str
    relation_type: str
    metadata: Optional[Dict] = None
    confidence_score: Optional[float] = None
    last_updated: Optional[str] = None

class MCPMemoryInterface:
    """
    Interface for interacting with MCP Memory server
    Specialized for legal knowledge graph management
    """
    
    def __init__(self):
        self.legal_entities = {}
        self.legal_relations = []
        self.verification_cache = {}
        
        # Initialize with core legal entities from the case
        self._initialize_core_entities()
    
    def _initialize_core_entities(self) -> None:
        """Initialize core legal entities from the user's case"""
        core_entities = [
            LegalEntity(
                name="Helen Haney Lafferty",
                entity_type="OpposingCounsel",
                observations=[
                    "Attorney at Klehr Harrison law firm",
                    "Filed Entry of Appearance on June 24, 2025",
                    "Represents plaintiff Melissa in divorce case",
                    "Transitioned from Weber Gallagher representation",
                    "Strategic escalation indicated by firm change"
                ],
                confidence_score=1.0,
                last_updated=datetime.now().isoformat()
            ),
            LegalEntity(
                name="Financial Abandonment Doctrine",
                entity_type="LegalMisinformation",
                observations=[
                    "VERIFIED FALSE by legal research - No such doctrine exists in PA",
                    "Appears incorrectly in user documents",
                    "Correct legal standard: 23 Pa.C.S. § 3301(a)(1) abandonment",
                    "Must be corrected in any legal strategy",
                    "Common misconception in pro se documentation"
                ],
                confidence_score=0.95,
                last_updated=datetime.now().isoformat()
            ),
            LegalEntity(
                name="Delaware County Family Court",
                entity_type="Jurisdiction",
                observations=[
                    "Prefers settlement-oriented approaches",
                    "Structured case management system",
                    "Male defendants may face unconscious bias per user analysis",
                    "Weber Gallagher shows stronger local specialization than Klehr Harrison",
                    "Media Family Court location in Delaware County"
                ],
                confidence_score=0.9,
                last_updated=datetime.now().isoformat()
            ),
            LegalEntity(
                name="Melissa Bemer",
                entity_type="Plaintiff",
                observations=[
                    "Plaintiff in divorce case - one of the main parties",
                    "Represented by Helen Haney Lafferty",
                    "Previously represented by Weber Gallagher",
                    "Subject of alleged abandonment claims",
                    "Employment status changes documented",
                    "Party to the legal case"
                ],
                confidence_score=1.0,
                last_updated=datetime.now().isoformat()
            ),
            LegalEntity(
                name="Stephen Boerner",
                entity_type="Defendant",
                observations=[
                    "Defendant in divorce case, proceeding pro se - one of the main parties",
                    "Family law attorney by profession",
                    "PTSD and ADHD medical documentation",
                    "Alleges medical and financial abandonment",
                    "Currently unemployable due to medical conditions",
                    "Party to the legal case"
                ],
                confidence_score=1.0,
                last_updated=datetime.now().isoformat()
            ),
            LegalEntity(
                name="23 Pa.C.S. § 3301(a)(1)",
                entity_type="Statute",
                observations=[
                    "Pennsylvania divorce grounds statute",
                    "Covers abandonment as grounds for divorce",
                    "Does not include 'financial abandonment doctrine'",
                    "Authoritative source for abandonment claims",
                    "Current as of 2024-2025"
                ],
                confidence_score=1.0,
                last_updated=datetime.now().isoformat()
            )
        ]
        
        # Store core entities
        for entity in core_entities:
            self.legal_entities[entity.name] = entity
        
        # Initialize core relationships
        core_relations = [
            LegalRelation(
                from_entity="Helen Haney Lafferty",
                to_entity="Klehr Harrison",
                relation_type="worksAt",
                confidence_score=1.0,
                last_updated=datetime.now().isoformat()
            ),
            LegalRelation(
                from_entity="Melissa Bemer",
                to_entity="Helen Haney Lafferty",
                relation_type="representedBy",
                confidence_score=1.0,
                last_updated=datetime.now().isoformat()
            ),
            LegalRelation(
                from_entity="Financial Abandonment Doctrine",
                to_entity="Pennsylvania Family Law",
                relation_type="contradicts",
                confidence_score=0.95,
                last_updated=datetime.now().isoformat()
            ),
            LegalRelation(
                from_entity="Stephen Boerner",
                to_entity="Delaware County Family Court",
                relation_type="litigatesIn",
                confidence_score=1.0,
                last_updated=datetime.now().isoformat()
            )
        ]
        
        self.legal_relations = core_relations
        
        logger.info(f"✅ Initialized {len(core_entities)} core legal entities and {len(core_relations)} relationships")
    
    def create_legal_entity(self, name: str, entity_type: str, observations: List[str], 
                           metadata: Optional[Dict] = None, confidence_score: float = 0.8) -> bool:
        """Create a new legal entity in the knowledge graph"""
        try:
            entity = LegalEntity(
                name=name,
                entity_type=entity_type,
                observations=observations,
                metadata=metadata or {},
                confidence_score=confidence_score,
                last_updated=datetime.now().isoformat()
            )
            
            self.legal_entities[name] = entity
            logger.info(f"✅ Created legal entity: {name} ({entity_type})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creating legal entity {name}: {e}")
            return False
    
    def add_observations_to_entity(self, entity_name: str, new_observations: List[str]) -> bool:
        """Add new observations to an existing legal entity"""
        try:
            if entity_name not in self.legal_entities:
                logger.warning(f"⚠️ Entity {entity_name} not found, creating new entity")
                return self.create_legal_entity(
                    name=entity_name,
                    entity_type="Unknown",
                    observations=new_observations
                )
            
            entity = self.legal_entities[entity_name]
            
            # Add new observations, avoiding duplicates
            for obs in new_observations:
                if obs not in entity.observations:
                    entity.observations.append(obs)
            
            entity.last_updated = datetime.now().isoformat()
            
            logger.info(f"✅ Added {len(new_observations)} observations to {entity_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error adding observations to {entity_name}: {e}")
            return False
    
    def create_legal_relation(self, from_entity: str, to_entity: str, relation_type: str,
                             metadata: Optional[Dict] = None, confidence_score: float = 0.8) -> bool:
        """Create a relationship between legal entities"""
        try:
            relation = LegalRelation(
                from_entity=from_entity,
                to_entity=to_entity,
                relation_type=relation_type,
                metadata=metadata or {},
                confidence_score=confidence_score,
                last_updated=datetime.now().isoformat()
            )
            
            self.legal_relations.append(relation)
            logger.info(f"✅ Created relation: {from_entity} --{relation_type}--> {to_entity}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creating relation {from_entity} -> {to_entity}: {e}")
            return False
    
    def store_verification_result(self, claim: str, verification_result: Dict) -> bool:
        """Store legal fact-checking verification results"""
        try:
            # Create entity for the claim if it's false or problematic
            if verification_result.get('fact_check_result') == 'FALSE':
                entity_name = f"Misinformation: {claim[:50]}..."
                observations = [
                    f"FACT-CHECK RESULT: {verification_result.get('fact_check_result', 'UNKNOWN')}",
                    f"Verification: {verification_result.get('detailed_analysis', '')[:200]}...",
                    f"Source: Perplexity API verification",
                    f"Confidence: {verification_result.get('confidence_score', 0.0)}",
                    "WARNING: Do not use this claim in legal documents"
                ]
                
                self.create_legal_entity(
                    name=entity_name,
                    entity_type="VerifiedMisinformation",
                    observations=observations,
                    metadata=verification_result,
                    confidence_score=verification_result.get('confidence_score', 0.9)
                )
            
            # Store in verification cache
            self.verification_cache[claim] = {
                'result': verification_result,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Stored verification result for: {claim[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error storing verification result: {e}")
            return False
    
    def search_entities(self, query: str, entity_type: Optional[str] = None) -> List[LegalEntity]:
        """Search for entities in the knowledge graph"""
        results = []
        query_lower = query.lower()
        
        for entity in self.legal_entities.values():
            # Check if entity type matches (if specified)
            if entity_type and entity.entity_type != entity_type:
                continue
            
            # Search in name
            if query_lower in entity.name.lower():
                results.append(entity)
                continue
            
            # Search in observations
            for obs in entity.observations:
                if query_lower in obs.lower():
                    results.append(entity)
                    break
        
        # Sort by confidence score
        results.sort(key=lambda x: x.confidence_score or 0, reverse=True)
        return results
    
    def get_entity_relationships(self, entity_name: str) -> List[LegalRelation]:
        """Get all relationships for a specific entity"""
        relationships = []
        
        for relation in self.legal_relations:
            if relation.from_entity == entity_name or relation.to_entity == entity_name:
                relationships.append(relation)
        
        return relationships
    
    def get_cached_verification(self, claim: str) -> Optional[Dict]:
        """Get cached verification result for a claim"""
        return self.verification_cache.get(claim)
    
    def store_delaware_county_intelligence(self, topic: str, intelligence: Dict) -> bool:
        """Store Delaware County specific strategic intelligence"""
        try:
            entity_name = f"Delaware County Strategy: {topic}"
            observations = [
                f"Strategic intelligence for: {topic}",
                f"Research date: {datetime.now().strftime('%Y-%m-%d')}",
                f"Source: Delaware County family court research"
            ]
            
            # Add key insights from intelligence
            if 'strategic_intelligence' in intelligence:
                insights = intelligence['strategic_intelligence'][:500]  # First 500 chars
                observations.append(f"Key insights: {insights}")
            
            return self.create_legal_entity(
                name=entity_name,
                entity_type="DelawareCountyIntelligence",
                observations=observations,
                metadata=intelligence,
                confidence_score=intelligence.get('confidence_score', 0.8)
            )
            
        except Exception as e:
            logger.error(f"❌ Error storing Delaware County intelligence: {e}")
            return False
    
    def store_precedent_research(self, legal_issue: str, research_result: Dict) -> bool:
        """Store precedent case research results"""
        try:
            entity_name = f"Precedent Research: {legal_issue}"
            observations = [
                f"Legal issue: {legal_issue}",
                f"Research date: {datetime.now().strftime('%Y-%m-%d')}",
                f"Jurisdiction: {research_result.get('jurisdiction', 'Pennsylvania')}",
                "Source: Legal precedent research"
            ]
            
            # Add key findings
            if 'precedent_analysis' in research_result:
                analysis = research_result['precedent_analysis'][:500]
                observations.append(f"Key findings: {analysis}")
            
            return self.create_legal_entity(
                name=entity_name,
                entity_type="PrecedentResearch",
                observations=observations,
                metadata=research_result,
                confidence_score=research_result.get('confidence_score', 0.8)
            )
            
        except Exception as e:
            logger.error(f"❌ Error storing precedent research: {e}")
            return False
    
    def get_misinformation_alerts(self) -> List[LegalEntity]:
        """Get all entities marked as misinformation"""
        return [entity for entity in self.legal_entities.values() 
                if entity.entity_type in ["LegalMisinformation", "VerifiedMisinformation"]]
    
    def get_knowledge_summary(self) -> Dict:
        """Get summary of the legal knowledge graph"""
        entity_types = {}
        relation_types = {}
        
        for entity in self.legal_entities.values():
            entity_types[entity.entity_type] = entity_types.get(entity.entity_type, 0) + 1
        
        for relation in self.legal_relations:
            relation_types[relation.relation_type] = relation_types.get(relation.relation_type, 0) + 1
        
        return {
            "total_entities": len(self.legal_entities),
            "total_relations": len(self.legal_relations),
            "entity_types": entity_types,
            "relation_types": relation_types,
            "cached_verifications": len(self.verification_cache),
            "misinformation_alerts": len(self.get_misinformation_alerts()),
            "last_updated": datetime.now().isoformat()
        }
    
    def get_knowledge_graph(self) -> Dict:
        """Get complete knowledge graph data for visualization"""
        try:
            # Convert entities to list format for frontend
            entities_list = []
            for entity in self.legal_entities.values():
                entities_list.append({
                    "name": entity.name,
                    "entityType": entity.entity_type,
                    "observations": entity.observations,
                    "metadata": entity.metadata,
                    "confidence_score": entity.confidence_score,
                    "last_updated": entity.last_updated
                })
            
            # Convert relations to list format for frontend
            relations_list = []
            for relation in self.legal_relations:
                relations_list.append({
                    "from": relation.from_entity,
                    "to": relation.to_entity,
                    "relationType": relation.relation_type,
                    "metadata": relation.metadata,
                    "confidence_score": relation.confidence_score,
                    "last_updated": relation.last_updated
                })
            
            return {
                "entities": entities_list,
                "relations": relations_list,
                "summary": self.get_knowledge_summary()
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting knowledge graph: {e}")
            return {
                "entities": [],
                "relations": [],
                "summary": {"error": str(e)}
            }
    
    def export_knowledge_graph(self, output_file: str = "legal_knowledge_graph.json") -> bool:
        """Export the entire knowledge graph to JSON"""
        try:
            # Convert dataclasses to dictionaries
            entities_dict = {}
            for name, entity in self.legal_entities.items():
                entities_dict[name] = {
                    "name": entity.name,
                    "entity_type": entity.entity_type,
                    "observations": entity.observations,
                    "metadata": entity.metadata,
                    "confidence_score": entity.confidence_score,
                    "last_updated": entity.last_updated
                }
            
            relations_list = []
            for relation in self.legal_relations:
                relations_list.append({
                    "from_entity": relation.from_entity,
                    "to_entity": relation.to_entity,
                    "relation_type": relation.relation_type,
                    "metadata": relation.metadata,
                    "confidence_score": relation.confidence_score,
                    "last_updated": relation.last_updated
                })
            
            knowledge_graph = {
                "entities": entities_dict,
                "relations": relations_list,
                "verification_cache": self.verification_cache,
                "export_timestamp": datetime.now().isoformat(),
                "summary": self.get_knowledge_summary()
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(knowledge_graph, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Exported knowledge graph to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error exporting knowledge graph: {e}")
            return False
    
    def import_knowledge_graph(self, input_file: str) -> bool:
        """Import knowledge graph from JSON file"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Import entities
            for name, entity_data in data.get("entities", {}).items():
                entity = LegalEntity(
                    name=entity_data["name"],
                    entity_type=entity_data["entity_type"],
                    observations=entity_data["observations"],
                    metadata=entity_data.get("metadata"),
                    confidence_score=entity_data.get("confidence_score"),
                    last_updated=entity_data.get("last_updated")
                )
                self.legal_entities[name] = entity
            
            # Import relations
            self.legal_relations = []
            for relation_data in data.get("relations", []):
                relation = LegalRelation(
                    from_entity=relation_data["from_entity"],
                    to_entity=relation_data["to_entity"],
                    relation_type=relation_data["relation_type"],
                    metadata=relation_data.get("metadata"),
                    confidence_score=relation_data.get("confidence_score"),
                    last_updated=relation_data.get("last_updated")
                )
                self.legal_relations.append(relation)
            
            # Import verification cache
            self.verification_cache = data.get("verification_cache", {})
            
            logger.info(f"✅ Imported knowledge graph from {input_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error importing knowledge graph: {e}")
            return False

# Test the MCP interface if run directly
if __name__ == "__main__":
    mcp = MCPMemoryInterface()
    
    print("🧪 Testing MCP Memory Interface...")
    
    # Test 1: Check initial entities
    print("\n1. Initial Knowledge Summary:")
    summary = mcp.get_knowledge_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    # Test 2: Search entities
    print("\n2. Searching for 'Helen'...")
    results = mcp.search_entities("Helen")
    for entity in results:
        print(f"Found: {entity.name} ({entity.entity_type})")
    
    # Test 3: Add new observation
    print("\n3. Adding observation to Helen Lafferty...")
    mcp.add_observations_to_entity(
        "Helen Haney Lafferty", 
        ["Test observation added during development"]
    )
    
    # Test 4: Check misinformation alerts
    print("\n4. Misinformation Alerts:")
    alerts = mcp.get_misinformation_alerts()
    for alert in alerts:
        print(f"⚠️ {alert.name}: {alert.observations[0]}")
    
    # Test 5: Export knowledge graph
    print("\n5. Exporting knowledge graph...")
    mcp.export_knowledge_graph("test_legal_knowledge_graph.json")
    
    print("\n✅ MCP Memory Interface testing completed!")