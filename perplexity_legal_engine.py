#!/usr/bin/env python3

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerplexityLegalEngine:
    """
    Advanced legal research and fact-checking engine using Perplexity API
    Specialized for Pennsylvania family law and Delaware County procedures
    """
    
    def __init__(self, api_key: str = "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"):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.cost_tracker = {
            "total_spent": 0.0,
            "queries_made": 0,
            "start_time": datetime.now().isoformat()
        }
        self.rate_limit_delay = 1.0  # seconds between requests
        
    def _make_request(self, messages: List[Dict], model: str = "llama-3.1-sonar-small-128k-online") -> Dict:
        """Make request to Perplexity API with error handling and cost tracking"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.2,
            "return_citations": True,
            "search_domain_filter": ["perplexity.ai"],
            "return_images": False
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            # Update cost tracking (estimated)
            self.cost_tracker["queries_made"] += 1
            self.cost_tracker["total_spent"] += 0.02  # Estimated cost per query
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Perplexity API request failed: {e}")
            return {"error": str(e)}
    
    def verify_legal_doctrine(self, doctrine_name: str, jurisdiction: str = "Pennsylvania") -> Dict:
        """
        Verify if a legal doctrine actually exists in specified jurisdiction
        Critical for detecting misinformation in user documents
        """
        messages = [
            {
                "role": "system",
                "content": "You are a legal research expert specializing in Pennsylvania family law. Provide authoritative, citation-backed responses about legal doctrines and statutes."
            },
            {
                "role": "user", 
                "content": f"""
                LEGAL VERIFICATION REQUEST - {jurisdiction} Family Law:
                
                Does "{doctrine_name}" exist as a recognized legal doctrine in {jurisdiction} divorce/family law?
                
                Please provide:
                1. TRUE/FALSE determination
                2. If FALSE: Explain why it doesn't exist and what might be confused with it
                3. If TRUE: Provide specific statute citations and relevant case law
                4. Alternative legal concepts that might apply instead
                5. Current 2024-2025 {jurisdiction} law on related topics
                
                Requirements: 
                - Use only official {jurisdiction} statutes, court rules, and authoritative case law
                - Cite specific statute numbers (e.g., 23 Pa.C.S. § 3301)
                - Include relevant court rules (e.g., Pa.R.C.P. 1920.XX)
                - Distinguish between legal concepts and non-existent doctrines
                """
            }
        ]
        
        response = self._make_request(messages)
        
        if "error" in response:
            return {"verification_status": "ERROR", "error": response["error"]}
        
        try:
            content = response["choices"][0]["message"]["content"]
            citations = response.get("citations", [])
            
            # Parse the TRUE/FALSE determination
            is_valid = "TRUE" in content.upper()[:200]  # Check first 200 chars for determination
            
            return {
                "doctrine_name": doctrine_name,
                "jurisdiction": jurisdiction,
                "verification_status": "VERIFIED" if is_valid else "FALSE",
                "is_valid_doctrine": is_valid,
                "explanation": content,
                "citations": citations,
                "confidence_score": 0.9 if citations else 0.7,
                "timestamp": datetime.now().isoformat(),
                "query_cost": 0.02
            }
            
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing Perplexity response: {e}")
            return {"verification_status": "PARSE_ERROR", "error": str(e)}
    
    def research_delaware_county_strategy(self, case_type: str, issue: str) -> Dict:
        """
        Get Delaware County specific strategic intelligence for family law cases
        """
        messages = [
            {
                "role": "system",
                "content": "You are a Pennsylvania family law expert with specific knowledge of Delaware County Court of Common Pleas procedures and practices."
            },
            {
                "role": "user",
                "content": f"""
                Delaware County, Pennsylvania Family Court Strategic Research:
                
                Case Type: {case_type}
                Specific Issue: {issue}
                
                Please provide current information on:
                1. Delaware County local court rules and procedures for this case type
                2. Judicial preferences and tendencies in Delaware County family court
                3. Strategic considerations specific to this jurisdiction
                4. Recent procedural changes or local practices (2024-2025)
                5. Success factors for pro se litigants in Delaware County
                6. Timing considerations and scheduling practices
                7. Settlement vs. litigation preferences in this jurisdiction
                
                Focus on practical, actionable intelligence that would help a pro se litigant navigate Delaware County family court effectively.
                """
            }
        ]
        
        response = self._make_request(messages)
        
        if "error" in response:
            return {"research_status": "ERROR", "error": response["error"]}
        
        try:
            content = response["choices"][0]["message"]["content"]
            citations = response.get("citations", [])
            
            return {
                "case_type": case_type,
                "issue": issue,
                "jurisdiction": "Delaware County, PA",
                "research_status": "COMPLETED",
                "strategic_intelligence": content,
                "citations": citations,
                "confidence_score": 0.85 if citations else 0.7,
                "timestamp": datetime.now().isoformat(),
                "query_cost": 0.02
            }
            
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing Delaware County research response: {e}")
            return {"research_status": "PARSE_ERROR", "error": str(e)}
    
    def research_precedent_cases(self, legal_issue: str, jurisdiction: str = "Pennsylvania") -> Dict:
        """
        Research relevant precedent cases for specific legal issues
        """
        messages = [
            {
                "role": "system", 
                "content": f"You are a legal research expert specializing in {jurisdiction} case law research and precedent analysis."
            },
            {
                "role": "user",
                "content": f"""
                PRECEDENT CASE RESEARCH - {jurisdiction}:
                
                Legal Issue: {legal_issue}
                
                Please find and analyze:
                1. Relevant {jurisdiction} Supreme Court cases
                2. {jurisdiction} Superior Court decisions
                3. Key holdings and legal principles established
                4. How these precedents apply to the legal issue
                5. Any distinguishing factors or limitations
                6. Recent developments or changes in the law (2024-2025)
                
                Provide specific case citations, holdings, and practical applications.
                Focus on cases that would be most persuasive in current litigation.
                """
            }
        ]
        
        response = self._make_request(messages)
        
        if "error" in response:
            return {"research_status": "ERROR", "error": response["error"]}
        
        try:
            content = response["choices"][0]["message"]["content"]
            citations = response.get("citations", [])
            
            return {
                "legal_issue": legal_issue,
                "jurisdiction": jurisdiction,
                "research_status": "COMPLETED",
                "precedent_analysis": content,
                "citations": citations,
                "confidence_score": 0.9 if citations else 0.75,
                "timestamp": datetime.now().isoformat(),
                "query_cost": 0.02
            }
            
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing precedent research response: {e}")
            return {"research_status": "PARSE_ERROR", "error": str(e)}
    
    def fact_check_legal_claim(self, claim: str, context: str = "") -> Dict:
        """
        Comprehensive fact-checking of legal claims against authoritative sources
        """
        messages = [
            {
                "role": "system",
                "content": "You are a legal fact-checker specializing in Pennsylvania family law. Your job is to verify legal claims against authoritative sources and identify misinformation."
            },
            {
                "role": "user",
                "content": f"""
                LEGAL FACT-CHECK REQUEST:
                
                Claim to Verify: "{claim}"
                Context: {context}
                
                Please provide:
                1. FACT-CHECK RESULT: TRUE, FALSE, or PARTIALLY TRUE
                2. EXPLANATION: Detailed reasoning for your determination
                3. AUTHORITATIVE SOURCES: Specific statutes, court rules, or case law
                4. CORRECTIONS: If false, provide the correct legal information
                5. RISK ASSESSMENT: What happens if this incorrect claim is used in court
                6. ALTERNATIVES: Better legal arguments or approaches if applicable
                
                Be extremely thorough and cite specific legal authorities.
                This is for a pro se litigant who needs accurate legal information.
                """
            }
        ]
        
        response = self._make_request(messages)
        
        if "error" in response:
            return {"fact_check_status": "ERROR", "error": response["error"]}
        
        try:
            content = response["choices"][0]["message"]["content"]
            citations = response.get("citations", [])
            
            # Determine fact-check result
            fact_check_result = "UNKNOWN"
            if "TRUE" in content.upper()[:300]:
                fact_check_result = "TRUE"
            elif "FALSE" in content.upper()[:300]:
                fact_check_result = "FALSE"
            elif "PARTIALLY TRUE" in content.upper()[:300]:
                fact_check_result = "PARTIALLY_TRUE"
            
            return {
                "original_claim": claim,
                "context": context,
                "fact_check_status": "COMPLETED",
                "fact_check_result": fact_check_result,
                "detailed_analysis": content,
                "citations": citations,
                "confidence_score": 0.9 if citations else 0.7,
                "timestamp": datetime.now().isoformat(),
                "query_cost": 0.02
            }
            
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing fact-check response: {e}")
            return {"fact_check_status": "PARSE_ERROR", "error": str(e)}
    
    def get_cost_summary(self) -> Dict:
        """Get current usage and cost summary"""
        return {
            "total_queries": self.cost_tracker["queries_made"],
            "estimated_cost": self.cost_tracker["total_spent"],
            "remaining_budget": 25.0 - self.cost_tracker["total_spent"],
            "start_time": self.cost_tracker["start_time"],
            "cost_per_query": 0.02
        }
    
    def batch_verify_claims(self, claims: List[str], context: str = "") -> List[Dict]:
        """
        Batch verification of multiple legal claims
        Optimized for cost efficiency
        """
        results = []
        
        logger.info(f"Starting batch verification of {len(claims)} claims")
        
        for i, claim in enumerate(claims, 1):
            logger.info(f"Verifying claim {i}/{len(claims)}: {claim[:50]}...")
            
            result = self.fact_check_legal_claim(claim, context)
            results.append(result)
            
            # Add delay between requests for rate limiting
            if i < len(claims):
                time.sleep(self.rate_limit_delay)
        
        logger.info(f"Batch verification completed. Total cost: ${len(claims) * 0.02:.2f}")
        
        return results

# Test the engine if run directly
if __name__ == "__main__":
    # Initialize the engine
    engine = PerplexityLegalEngine()
    
    print("🧪 Testing Perplexity Legal Engine...")
    
    # Test 1: Verify a known false doctrine
    print("\n1. Testing verification of false doctrine...")
    result = engine.verify_legal_doctrine("financial abandonment doctrine")
    print(f"Result: {result['verification_status']}")
    print(f"Valid: {result.get('is_valid_doctrine', 'Unknown')}")
    
    # Test 2: Delaware County research
    print("\n2. Testing Delaware County research...")
    result = engine.research_delaware_county_strategy("divorce", "property division")
    print(f"Research Status: {result['research_status']}")
    
    # Test 3: Cost summary
    print("\n3. Cost Summary:")
    costs = engine.get_cost_summary()
    print(f"Queries made: {costs['total_queries']}")
    print(f"Estimated cost: ${costs['estimated_cost']:.2f}")
    print(f"Remaining budget: ${costs['remaining_budget']:.2f}")
    
    print("\n✅ Perplexity Legal Engine testing completed!")