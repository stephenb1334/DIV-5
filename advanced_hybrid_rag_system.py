#!/usr/bin/env python3

import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Import our custom components
from perplexity_legal_engine import PerplexityLegalEngine
from comprehensive_document_processor import ComprehensiveDocumentProcessor
from mcp_memory_interface import MCPMemoryInterface

# Original Nomic Atlas imports
from nomic import atlas
import openai

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    """Unified search result from any source"""
    content: str
    source: str  # 'local', 'atlas', 'perplexity', 'memory'
    category: str
    relevance_score: float
    metadata: Dict
    verification_status: Optional[str] = None
    confidence_score: Optional[float] = None
    misinformation_alert: Optional[str] = None

@dataclass
class ConfidenceRecommendation:
    """Recommendation to improve confidence score"""
    current_confidence: float
    target_confidence: float
    recommended_actions: List[str]
    estimated_improvement: float
    cost_estimate: float

@dataclass
class HybridRAGResponse:
    """Complete response from the hybrid RAG system"""
    query: str
    search_results: List[SearchResult]
    ai_response: str
    fact_check_results: List[Dict]
    misinformation_alerts: List[str]
    strategic_advice: Optional[str]
    sources_used: List[str]
    confidence_score: float
    cost_breakdown: Dict
    timestamp: str
    confidence_recommendation: Optional[ConfidenceRecommendation] = None
    formatted_results: Optional[List[Dict]] = None

class AdvancedHybridRAGSystem:
    """
    Advanced Hybrid RAG System integrating:
    - Local document processing (all 500+ files)
    - Nomic Atlas visualization and embeddings
    - Perplexity API fact-checking
    - MCP Memory knowledge graph
    - Pro se protection features
    """
    
    def __init__(self):
        # Initialize all components
        self.perplexity_engine = PerplexityLegalEngine()
        self.document_processor = ComprehensiveDocumentProcessor()
        self.mcp_memory = MCPMemoryInterface()
        
        # Atlas configuration
        self.atlas_dataset_id = "talon-pro-se/stephen-boerner-divorce-case-data-test-upload"
        self.atlas_documents_df = None
        
        # OpenAI configuration for response generation
        self.openrouter_client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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"
        )
        
        # Local document storage
        self.local_documents = []
        self.local_embeddings = {}
        
        # System state
        self.is_initialized = False
        self.initialization_log = []
        
        # Initialize all systems
        self._initialize_systems()
    
    def _initialize_systems(self) -> None:
        """Initialize all RAG system components"""
        logger.info("🚀 Initializing Advanced Hybrid RAG System...")
        
        try:
            # 1. Load Nomic Atlas data
            self._load_atlas_data()
            
            # 2. Process local documents (process ALL documents)
            self._process_local_documents(max_files=None)  # Process ALL files
            
            # 3. Initialize MCP Memory with verification results
            self._initialize_legal_knowledge()
            
            self.is_initialized = True
            logger.info("✅ Advanced Hybrid RAG System initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error initializing hybrid RAG system: {e}")
            self.initialization_log.append(f"ERROR: {e}")
    
    def _load_atlas_data(self) -> None:
        """Load data from Nomic Atlas"""
        try:
            logger.info("🔄 Loading data from Nomic Atlas...")
            dataset = atlas.AtlasDataset(identifier=self.atlas_dataset_id)
            first_map = dataset.maps[0]
            self.atlas_documents_df = first_map.data.df
            logger.info(f"✅ Loaded {len(self.atlas_documents_df)} documents from Atlas")
            self.initialization_log.append(f"Atlas: {len(self.atlas_documents_df)} documents loaded")
            
        except Exception as e:
            logger.error(f"❌ Error loading Atlas data: {e}")
            self.initialization_log.append(f"Atlas ERROR: {e}")
    
    def _process_local_documents(self, max_files: Optional[int] = None) -> None:
        """Process local documents for comprehensive search"""
        try:
            logger.info("📄 Processing local documents...")
            
            # Process documents
            self.local_documents = self.document_processor.process_all_documents(max_files=max_files)
            
            logger.info(f"✅ Processed {len(self.local_documents)} local documents")
            self.initialization_log.append(f"Local: {len(self.local_documents)} documents processed")
            
            # Extract and store potential legal claims for fact-checking
            self._extract_legal_claims_for_verification()
            
        except Exception as e:
            logger.error(f"❌ Error processing local documents: {e}")
            self.initialization_log.append(f"Local processing ERROR: {e}")
    
    def _extract_legal_claims_for_verification(self) -> None:
        """Extract legal claims from documents for batch verification"""
        try:
            all_claims = set()
            
            for doc in self.local_documents:
                if 'metadata' in doc and 'legal_claims' in doc['metadata']:
                    all_claims.update(doc['metadata']['legal_claims'])
            
            # Prioritize potential misinformation
            priority_claims = [claim for claim in all_claims 
                             if any(keyword in claim.lower() 
                                   for keyword in ['abandonment doctrine', 'financial abandonment'])]
            
            if priority_claims:
                logger.info(f"⚠️ Found {len(priority_claims)} priority claims for verification")
                
                # Store for later verification (don't verify all at once to save costs)
                for claim in priority_claims[:5]:  # Verify top 5 priority claims
                    self.mcp_memory.verification_cache[claim] = {
                        'status': 'pending_verification',
                        'priority': 'high',
                        'found_in_documents': True
                    }
            
        except Exception as e:
            logger.error(f"❌ Error extracting legal claims: {e}")
    
    def _initialize_legal_knowledge(self) -> None:
        """Initialize legal knowledge graph with key information"""
        try:
            logger.info("🧠 Initializing legal knowledge graph...")
            
            # The MCP Memory interface already initializes core entities
            summary = self.mcp_memory.get_knowledge_summary()
            logger.info(f"✅ Knowledge graph initialized: {summary['total_entities']} entities, {summary['total_relations']} relations")
            self.initialization_log.append(f"MCP Memory: {summary['total_entities']} entities initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing legal knowledge: {e}")
            self.initialization_log.append(f"MCP Memory ERROR: {e}")
    
    def hybrid_search(self, query: str, search_mode: str = "comprehensive", 
                     max_results: int = 10, enable_fact_check: bool = True) -> List[SearchResult]:
        """
        Perform hybrid search across all data sources
        
        Args:
            query: User's search query
            search_mode: 'local', 'atlas', 'memory', 'comprehensive'
            max_results: Maximum number of results to return
            enable_fact_check: Whether to perform fact-checking
        """
        results = []
        
        try:
            if search_mode in ['local', 'comprehensive']:
                local_results = self._search_local_documents(query, max_results)
                results.extend(local_results)
            
            if search_mode in ['atlas', 'comprehensive']:
                atlas_results = self._search_atlas_documents(query, max_results)
                results.extend(atlas_results)
            
            if search_mode in ['memory', 'comprehensive']:
                memory_results = self._search_memory_graph(query, max_results)
                results.extend(memory_results)
            
            # Enhanced sorting for party/attorney queries
            query_lower = query.lower()
            party_keywords = ['parties', 'party', 'plaintiff', 'defendant', 'attorney', 'counsel', 'lawyer', 'opposing']
            is_party_query = any(keyword in query_lower for keyword in party_keywords)
            
            if is_party_query:
                # Prioritize Memory results with party information
                def sort_key(result):
                    priority_score = result.relevance_score
                    
                    # Boost Memory source results for party queries
                    if result.source == 'memory' and result.metadata.get('is_party_info', False):
                        priority_score += 0.5
                    
                    # Boost any result that contains party information
                    if any(entity_type in result.category for entity_type in ['Plaintiff', 'Defendant', 'OpposingCounsel']):
                        priority_score += 0.3
                    
                    return priority_score
                
                results.sort(key=sort_key, reverse=True)
            else:
                # Standard sorting by relevance score
                results.sort(key=lambda x: x.relevance_score, reverse=True)
            
            # Limit results
            results = results[:max_results]
            
            # Perform fact-checking if enabled
            if enable_fact_check:
                results = self._add_fact_checking_to_results(results, query)
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Error in hybrid search: {e}")
            return []
    
    def _search_local_documents(self, query: str, max_results: int) -> List[SearchResult]:
        """Search local processed documents"""
        if not self.local_documents:
            return []
        
        try:
            # Extract text content for TF-IDF search
            texts = [doc.get('text', '')[:2000] for doc in self.local_documents]  # First 2000 chars
            
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            all_texts = texts + [query]
            tfidf_matrix = vectorizer.fit_transform(all_texts)
            
            # Calculate similarities
            query_vector = tfidf_matrix[-1]
            doc_vectors = tfidf_matrix[:-1]
            similarities = cosine_similarity(query_vector, doc_vectors).flatten()
            
            # Get top results
            top_indices = similarities.argsort()[-max_results:][::-1]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Minimum relevance threshold
                    doc = self.local_documents[idx]
                    
                    result = SearchResult(
                        content=doc.get('text', '')[:1000],  # First 1000 chars
                        source='local',
                        category=doc.get('category', 'Unknown'),
                        relevance_score=float(similarities[idx]),
                        metadata={
                            'filename': doc.get('filename', ''),
                            'file_path': doc.get('relative_path', ''),
                            'extension': doc.get('extension', ''),
                            'size_bytes': doc.get('size_bytes', 0),
                            'legal_metadata': doc.get('metadata', {})
                        }
                    )
                    results.append(result)
            
            logger.info(f"🔍 Local search found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error searching local documents: {e}")
            return []
    
    def _search_atlas_documents(self, query: str, max_results: int) -> List[SearchResult]:
        """Search Nomic Atlas documents"""
        if self.atlas_documents_df is None:
            return []
        
        try:
            # Use existing Atlas search logic
            texts = self.atlas_documents_df['text'].tolist()
            
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            all_texts = texts + [query]
            tfidf_matrix = vectorizer.fit_transform(all_texts)
            
            query_vector = tfidf_matrix[-1]
            doc_vectors = tfidf_matrix[:-1]
            similarities = cosine_similarity(query_vector, doc_vectors).flatten()
            
            top_indices = similarities.argsort()[-max_results:][::-1]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:
                    row = self.atlas_documents_df.iloc[idx]
                    
                    result = SearchResult(
                        content=str(row['text']),
                        source='atlas',
                        category=str(row.get('category', 'Atlas Document')),
                        relevance_score=float(similarities[idx]),
                        metadata={
                            'date_period': str(row.get('date_period', '')),
                            'source_document': str(row.get('source_document', '')),
                            'legal_theory_supported': str(row.get('legal_theory_supported', '')),
                            'contribution_type': str(row.get('contribution_type', ''))
                        }
                    )
                    results.append(result)
            
            logger.info(f"🗺️ Atlas search found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error searching Atlas documents: {e}")
            return []
    
    def _search_memory_graph(self, query: str, max_results: int) -> List[SearchResult]:
        """Search MCP Memory knowledge graph with enhanced party/attorney detection"""
        try:
            # Enhanced search for party/attorney queries
            query_lower = query.lower()
            party_keywords = ['parties', 'party', 'plaintiff', 'defendant', 'attorney', 'counsel', 'lawyer', 'opposing']
            
            # If asking about parties/attorneys, prioritize those entity types
            if any(keyword in query_lower for keyword in party_keywords):
                # Search for specific entity types first
                priority_types = ['Plaintiff', 'Defendant', 'OpposingCounsel', 'Attorney']
                priority_entities = []
                
                for entity_type in priority_types:
                    type_entities = self.mcp_memory.search_entities(query, entity_type=entity_type)
                    priority_entities.extend(type_entities)
                
                # Also get general search results
                general_entities = self.mcp_memory.search_entities(query)
                
                # Combine and deduplicate
                all_entities = priority_entities + [e for e in general_entities if e not in priority_entities]
            else:
                all_entities = self.mcp_memory.search_entities(query)
            
            results = []
            for entity in all_entities[:max_results]:
                # Enhanced content formatting for party information
                if entity.entity_type in ['Plaintiff', 'Defendant', 'OpposingCounsel']:
                    content = f"**{entity.entity_type.upper()}: {entity.name}**\n\n"
                    content += "Key Information:\n"
                    for i, obs in enumerate(entity.observations, 1):
                        content += f"{i}. {obs}\n"
                    
                    # Add relationship information
                    relationships = self.mcp_memory.get_entity_relationships(entity.name)
                    if relationships:
                        content += "\nRelationships:\n"
                        for rel in relationships:
                            if rel.from_entity == entity.name:
                                content += f"• {entity.name} {rel.relation_type} {rel.to_entity}\n"
                            else:
                                content += f"• {rel.from_entity} {rel.relation_type} {entity.name}\n"
                else:
                    content = f"Entity: {entity.name}\nType: {entity.entity_type}\n"
                    content += "\n".join(entity.observations)
                
                # Higher relevance score for party/attorney entities when asked about parties
                relevance_boost = 0.0
                if any(keyword in query_lower for keyword in party_keywords):
                    if entity.entity_type in ['Plaintiff', 'Defendant', 'OpposingCounsel']:
                        relevance_boost = 0.3
                
                result = SearchResult(
                    content=content,
                    source='memory',
                    category=f"Legal Entity - {entity.entity_type}",
                    relevance_score=min(1.0, (entity.confidence_score or 0.8) + relevance_boost),
                    metadata={
                        'entity_name': entity.name,
                        'entity_type': entity.entity_type,
                        'last_updated': entity.last_updated,
                        'stored_metadata': entity.metadata,
                        'is_party_info': entity.entity_type in ['Plaintiff', 'Defendant', 'OpposingCounsel']
                    },
                    confidence_score=entity.confidence_score
                )
                results.append(result)
            
            logger.info(f"🧠 Memory search found {len(results)} results (party-enhanced)")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error searching memory graph: {e}")
            return []
    
    def _add_fact_checking_to_results(self, results: List[SearchResult], query: str) -> List[SearchResult]:
        """Add fact-checking verification to search results"""
        try:
            # Extract potential legal claims from query and results
            claims_to_check = set()
            
            # Check query for legal claims
            query_lower = query.lower()
            if any(keyword in query_lower for keyword in ['doctrine', 'abandonment', 'precedent']):
                claims_to_check.add(query)
            
            # Check results for misinformation flags
            for result in results:
                if result.metadata.get('legal_metadata', {}).get('potential_misinformation'):
                    claims_to_check.update(result.metadata['legal_metadata']['potential_misinformation'])
            
            # Verify claims (limit to avoid excessive API costs)
            for claim in list(claims_to_check)[:3]:  # Only check top 3 claims
                # Check cache first
                cached_verification = self.mcp_memory.get_cached_verification(claim)
                
                if cached_verification:
                    # Use cached result
                    verification = cached_verification['result']
                else:
                    # Perform new verification
                    verification = self.perplexity_engine.fact_check_legal_claim(claim)
                    self.mcp_memory.store_verification_result(claim, verification)
                
                # Add verification to relevant results
                for result in results:
                    if claim.lower() in result.content.lower():
                        result.verification_status = verification.get('fact_check_result', 'UNKNOWN')
                        if verification.get('fact_check_result') == 'FALSE':
                            result.misinformation_alert = f"⚠️ MISINFORMATION DETECTED: {claim}"
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Error adding fact-checking: {e}")
            return results
    
    def generate_comprehensive_response(self, query: str, search_mode: str = "comprehensive",
                                      perplexity_enabled: bool = True) -> HybridRAGResponse:
        """Generate comprehensive response using all system components"""
        start_time = datetime.now()
        
        try:
            # 1. Perform hybrid search (adjust based on Perplexity availability)
            if not perplexity_enabled and search_mode == "perplexity":
                search_mode = "local"  # Fall back to local search
            
            search_results = self.hybrid_search(query, search_mode=search_mode, enable_fact_check=perplexity_enabled)
            
            # 2. Extract legal claims for verification (only if Perplexity enabled)
            fact_check_results = []
            if perplexity_enabled:
                claims_for_verification = self._extract_claims_from_query(query)
                
                for claim in claims_for_verification[:2]:  # Limit to 2 verifications per query
                    verification = self.perplexity_engine.fact_check_legal_claim(claim)
                    fact_check_results.append(verification)
                    self.mcp_memory.store_verification_result(claim, verification)
            
            # 3. Check for misinformation alerts
            misinformation_alerts = []
            for result in search_results:
                if result.misinformation_alert:
                    misinformation_alerts.append(result.misinformation_alert)
            
            # 4. Get strategic advice if relevant (only if Perplexity enabled)
            strategic_advice = None
            if perplexity_enabled and any(keyword in query.lower() for keyword in ['strategy', 'delaware county', 'court', 'tactics']):
                strategy_research = self.perplexity_engine.research_delaware_county_strategy(
                    "divorce", query
                )
                strategic_advice = strategy_research.get('strategic_intelligence', '')
                self.mcp_memory.store_delaware_county_intelligence(query, strategy_research)
            
            # 5. Generate AI response
            ai_response = self._generate_ai_response(query, search_results, fact_check_results, misinformation_alerts)
            
            # 6. Calculate confidence score
            confidence_score = self._calculate_confidence_score(search_results, fact_check_results)
            
            # 7. Generate confidence recommendations if score is below target
            confidence_recommendation = None
            if confidence_score < 0.95:  # Target 95% confidence
                confidence_recommendation = self._generate_confidence_recommendations(
                    confidence_score, search_results, fact_check_results, perplexity_enabled
                )
            
            # 8. Format search results for human-readable display
            formatted_results = self._format_search_results_for_display(search_results)
            
            # 9. Compile cost breakdown
            perplexity_queries = 0 if not perplexity_enabled else len(fact_check_results) + (1 if strategic_advice else 0)
            cost_breakdown = {
                'perplexity_queries': perplexity_queries,
                'estimated_cost': perplexity_queries * 0.02,
                'openai_tokens': 0,  # Would need to track actual token usage
                'perplexity_enabled': perplexity_enabled
            }
            
            # 10. Create comprehensive response
            response = HybridRAGResponse(
                query=query,
                search_results=search_results,
                ai_response=ai_response,
                fact_check_results=fact_check_results,
                misinformation_alerts=misinformation_alerts,
                strategic_advice=strategic_advice,
                sources_used=list(set(result.source for result in search_results)),
                confidence_score=confidence_score,
                cost_breakdown=cost_breakdown,
                timestamp=datetime.now().isoformat(),
                confidence_recommendation=confidence_recommendation,
                formatted_results=formatted_results
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"✅ Generated comprehensive response in {processing_time:.2f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error generating comprehensive response: {e}")
            return HybridRAGResponse(
                query=query,
                search_results=[],
                ai_response=f"An error occurred while processing your query: {e}",
                fact_check_results=[],
                misinformation_alerts=[],
                strategic_advice=None,
                sources_used=[],
                confidence_score=0.0,
                cost_breakdown={'error': str(e)},
                timestamp=datetime.now().isoformat()
            )
    
    def _extract_claims_from_query(self, query: str) -> List[str]:
        """Extract potential legal claims from user query for fact-checking"""
        claims = []
        
        # Common misinformation patterns
        misinformation_patterns = [
            r'financial abandonment doctrine',
            r'abandonment doctrine',
            r'medical abandonment doctrine'
        ]
        
        query_lower = query.lower()
        for pattern in misinformation_patterns:
            if pattern in query_lower:
                claims.append(pattern)
        
        # If query asks about specific legal concepts
        if any(word in query_lower for word in ['doctrine', 'law', 'statute', 'precedent']):
            claims.append(query)
        
        return claims
    
    def _generate_ai_response(self, query: str, search_results: List[SearchResult], 
                             fact_check_results: List[Dict], misinformation_alerts: List[str]) -> str:
        """Generate AI response using OpenRouter"""
        try:
            # Prepare context
            context_parts = []
            
            # Enhanced context preparation for party queries
            query_lower = query.lower()
            party_keywords = ['parties', 'party', 'plaintiff', 'defendant', 'attorney', 'counsel', 'lawyer', 'opposing']
            is_party_query = any(keyword in query_lower for keyword in party_keywords)
            
            # Add search results with enhanced formatting for party information
            for i, result in enumerate(search_results[:5], 1):  # Top 5 results
                context_part = f"Source {i} ({result.source}):\n"
                context_part += f"Category: {result.category}\n"
                
                # For party queries, show more content from Memory sources
                if is_party_query and result.source == 'memory' and result.metadata.get('is_party_info', False):
                    context_part += f"PARTY INFORMATION:\n{result.content}\n"
                else:
                    context_part += f"Content: {result.content[:500]}...\n"
                
                if result.verification_status:
                    context_part += f"Fact-check: {result.verification_status}\n"
                context_parts.append(context_part)
            
            # Add fact-check results
            if fact_check_results:
                context_parts.append("\nFACT-CHECK RESULTS:")
                for fc in fact_check_results:
                    context_parts.append(f"Claim: {fc.get('original_claim', '')}")
                    context_parts.append(f"Result: {fc.get('fact_check_result', '')}")
                    context_parts.append(f"Analysis: {fc.get('detailed_analysis', '')[:300]}...")
            
            # Add misinformation alerts
            if misinformation_alerts:
                context_parts.append("\nMISINFORMATION ALERTS:")
                context_parts.extend(misinformation_alerts)
            
            context_text = "\n---\n".join(context_parts)
            
            # Enhanced system message for party information queries
            query_lower = query.lower()
            party_keywords = ['parties', 'party', 'plaintiff', 'defendant', 'attorney', 'counsel', 'lawyer', 'opposing']
            is_party_query = any(keyword in query_lower for keyword in party_keywords)
            
            if is_party_query:
                system_message = """You are an expert legal AI assistant specializing in Pennsylvania divorce and family law with advanced fact-checking capabilities.

CRITICAL INSTRUCTIONS FOR PARTY/ATTORNEY QUERIES:
1. When asked about parties, attorneys, or counsel, provide SPECIFIC NAMES and details from the context
2. Extract and clearly present: Names, Roles (Plaintiff/Defendant), Attorney information, Law firms
3. Use the Legal Entity information from the Memory source as the PRIMARY source for party details
4. Format party information clearly with names, roles, and relationships
5. If context contains party information, DO NOT say "unable to provide specific information"
6. Prioritize Memory source results over other sources for party information

GENERAL INSTRUCTIONS:
1. Answer based ONLY on the provided verified context
2. If fact-check results show FALSE claims, clearly warn the user and provide corrections
3. Prioritize authoritative legal sources and current Pennsylvania law
4. For pro se litigants, emphasize accuracy and warn against misinformation
5. Cite specific sources, documents, and legal authorities when available

MISINFORMATION PROTECTION:
- Always flag any false legal doctrines or incorrect law
- Provide correct legal standards when correcting misinformation
- Warn about risks of using incorrect legal information in court
"""
            else:
                system_message = """You are an expert legal AI assistant specializing in Pennsylvania divorce and family law with advanced fact-checking capabilities.

CRITICAL INSTRUCTIONS:
1. Answer based ONLY on the provided verified context
2. If fact-check results show FALSE claims, clearly warn the user and provide corrections
3. Prioritize authoritative legal sources and current Pennsylvania law
4. For pro se litigants, emphasize accuracy and warn against misinformation
5. Cite specific sources, documents, and legal authorities when available
6. If context lacks sufficient information, state this clearly

MISINFORMATION PROTECTION:
- Always flag any false legal doctrines or incorrect law
- Provide correct legal standards when correcting misinformation
- Warn about risks of using incorrect legal information in court
"""
            
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Context from legal case documents and verification:\n\n{context_text}\n\nQuestion: {query}"}
            ]
            
            completion = self.openrouter_client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=messages,
                temperature=0.3,  # Lower temperature for legal accuracy
                max_tokens=1000
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"❌ Error generating AI response: {e}")
            return f"I encountered an error while generating a response. Please try rephrasing your question. Error: {e}"
    
    def _calculate_confidence_score(self, search_results: List[SearchResult],
                                  fact_check_results: List[Dict]) -> float:
        """Enhanced confidence score calculation with multiple factors"""
        if not search_results:
            return 0.0
        
        # 1. Base relevance score (40% weight)
        avg_relevance = sum(result.relevance_score for result in search_results) / len(search_results)
        relevance_component = avg_relevance * 0.4
        
        # 2. Source diversity bonus (20% weight)
        unique_sources = len(set(result.source for result in search_results))
        source_diversity = min(1.0, unique_sources / 3) * 0.2  # Max bonus for 3+ sources
        
        # 3. Result quantity factor (15% weight)
        result_quantity = min(1.0, len(search_results) / 10) * 0.15  # Max bonus for 10+ results
        
        # 4. Fact-checking verification (15% weight)
        fact_check_component = 0.0
        if fact_check_results:
            verified_claims = sum(1 for fc in fact_check_results if fc.get('fact_check_result') == 'TRUE')
            fact_check_component = (verified_claims / len(fact_check_results)) * 0.15
        
        # 5. Memory/Knowledge graph presence (10% weight)
        memory_bonus = 0.0
        memory_results = [r for r in search_results if r.source == 'memory']
        if memory_results:
            memory_bonus = min(1.0, len(memory_results) / 3) * 0.1
        
        # Penalties
        misinformation_penalty = 0.0
        for result in search_results:
            if result.misinformation_alert:
                misinformation_penalty += 0.15  # Reduced penalty, more nuanced
        
        # Calculate final confidence
        confidence = relevance_component + source_diversity + result_quantity + fact_check_component + memory_bonus - misinformation_penalty
        return min(1.0, max(0.0, confidence))
    
    def _generate_confidence_recommendations(self, current_confidence: float, search_results: List[SearchResult],
                                           fact_check_results: List[Dict], perplexity_enabled: bool) -> ConfidenceRecommendation:
        """Generate intelligent recommendations to improve confidence score"""
        target_confidence = 0.95
        recommendations = []
        estimated_improvement = 0.0
        cost_estimate = 0.0
        
        # Analyze current state
        unique_sources = len(set(result.source for result in search_results))
        result_count = len(search_results)
        has_fact_checking = len(fact_check_results) > 0
        memory_results = [r for r in search_results if r.source == 'memory']
        
        # Recommendation 1: Expand search results
        if result_count < 20:
            recommendations.append(f"🔍 Expand search from {result_count} to 20 results for broader coverage")
            estimated_improvement += 0.15
        
        # Recommendation 2: Enable Perplexity for fact-checking
        if not perplexity_enabled:
            recommendations.append("🌐 Enable Perplexity API for real-time fact-checking and verification")
            estimated_improvement += 0.20
            cost_estimate += 0.06  # ~3 queries at $0.02 each
        
        # Recommendation 3: Cross-reference multiple sources
        if unique_sources < 3:
            recommendations.append("📚 Search across all sources (Local + Atlas + Memory) for comprehensive coverage")
            estimated_improvement += 0.10
        
        # Recommendation 4: Enhance with strategic intelligence
        if not any('strategy' in r.content.lower() for r in search_results):
            recommendations.append("🎯 Access Delaware County strategic intelligence for jurisdiction-specific insights")
            estimated_improvement += 0.08
            cost_estimate += 0.02
        
        # Recommendation 5: Verify legal claims
        if not has_fact_checking and perplexity_enabled:
            recommendations.append("✅ Perform legal claim verification to ensure accuracy")
            estimated_improvement += 0.12
            cost_estimate += 0.04
        
        # Recommendation 6: Access knowledge graph relationships
        if len(memory_results) < 2:
            recommendations.append("🧠 Explore knowledge graph relationships for deeper context")
            estimated_improvement += 0.05
        
        return ConfidenceRecommendation(
            current_confidence=current_confidence,
            target_confidence=target_confidence,
            recommended_actions=recommendations,
            estimated_improvement=min(estimated_improvement, target_confidence - current_confidence),
            cost_estimate=cost_estimate
        )
    
    def _format_search_results_for_display(self, search_results: List[SearchResult]) -> List[Dict]:
        """Format search results for human-readable display"""
        formatted_results = []
        
        for i, result in enumerate(search_results, 1):
            # Determine display category and icon
            if result.source == 'memory':
                icon = "🧠"
                source_display = "Knowledge Graph"
            elif result.source == 'atlas':
                icon = "🗺️"
                source_display = "Atlas Documents"
            elif result.source == 'local':
                icon = "📄"
                source_display = "Local Documents"
            elif result.source == 'perplexity':
                icon = "🌐"
                source_display = "Perplexity Research"
            else:
                icon = "📋"
                source_display = result.source.title()
            
            # Format content based on source type
            if result.source == 'memory' and result.metadata.get('is_party_info', False):
                # Special formatting for party information
                content_preview = result.content[:300]
                content_type = "Party Information"
            elif result.source == 'local':
                # Format local document results
                content_preview = result.content[:250] + "..." if len(result.content) > 250 else result.content
                content_type = f"Document: {result.metadata.get('filename', 'Unknown')}"
            else:
                content_preview = result.content[:200] + "..." if len(result.content) > 200 else result.content
                content_type = result.category
            
            # Create formatted result
            formatted_result = {
                "rank": i,
                "icon": icon,
                "source": source_display,
                "content_type": content_type,
                "content_preview": content_preview,
                "relevance_score": round(result.relevance_score * 100, 1),
                "confidence_indicator": "🟢" if result.relevance_score > 0.7 else "🟡" if result.relevance_score > 0.4 else "🔴",
                "metadata": {
                    "filename": result.metadata.get('filename', ''),
                    "file_path": result.metadata.get('file_path', ''),
                    "entity_type": result.metadata.get('entity_type', ''),
                    "verification_status": result.verification_status,
                    "misinformation_alert": result.misinformation_alert
                },
                "full_content": result.content,
                "expandable": len(result.content) > 250
            }
            
            formatted_results.append(formatted_result)
        
        return formatted_results
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        atlas_status = len(self.atlas_documents_df) if self.atlas_documents_df is not None else 0
        local_status = len(self.local_documents)
        memory_status = self.mcp_memory.get_knowledge_summary()
        perplexity_status = self.perplexity_engine.get_cost_summary()
        
        return {
            "system_initialized": self.is_initialized,
            "initialization_log": self.initialization_log,
            "atlas_documents": atlas_status,
            "local_documents": local_status,
            "memory_entities": memory_status.get('total_entities', 0),
            "memory_relations": memory_status.get('total_relations', 0),
            "perplexity_queries": perplexity_status.get('total_queries', 0),
            "perplexity_cost": perplexity_status.get('estimated_cost', 0.0),
            "timestamp": datetime.now().isoformat()
        }

# Test the system if run directly
if __name__ == "__main__":
    system = AdvancedHybridRAGSystem()
    
    print("🧪 Testing Advanced Hybrid RAG System...")
    
    # Test 1: System status
    print("\n1. System Status:")
    status = system.get_system_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    
    # Test 2: Simple search
    print("\n2. Testing search for 'Helen Lafferty'...")
    results = system.hybrid_search("Helen Lafferty", max_results=3)
    for result in results:
        print(f"Source: {result.source}, Score: {result.relevance_score:.3f}")
        print(f"Content: {result.content[:100]}...")
    
    # Test 3: Comprehensive response
    print("\n3. Testing comprehensive response...")
    response = system.generate_comprehensive_response("Who is the opposing counsel?")
    print(f"AI Response: {response.ai_response[:200]}...")
    print(f"Sources used: {response.sources_used}")
    print(f"Confidence: {response.confidence_score:.3f}")
    
    print("\n✅ Advanced Hybrid RAG System testing completed!")