#!/usr/bin/env python3

import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
import traceback

# Import our advanced hybrid system
from advanced_hybrid_rag_system import AdvancedHybridRAGSystem

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Global system instance
hybrid_rag_system = None

def initialize_system():
    """Initialize the Advanced Hybrid RAG System"""
    global hybrid_rag_system
    try:
        logger.info("🚀 Initializing Enhanced Legal RAG Web Application...")
        hybrid_rag_system = AdvancedHybridRAGSystem()
        logger.info("✅ Enhanced Legal RAG System initialized successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Error initializing system: {e}")
        logger.error(traceback.format_exc())
        return False

@app.route('/')
def index():
    """Main page with enhanced interface"""
    try:
        # Get system status
        if hybrid_rag_system and hybrid_rag_system.is_initialized:
            status = hybrid_rag_system.get_system_status()
        else:
            status = {
                "system_initialized": False,
                "error": "System not initialized"
            }
        
        return render_template('enhanced_index.html', system_status=status)
    except Exception as e:
        logger.error(f"❌ Error loading index page: {e}")
        return render_template('enhanced_index.html', 
                             system_status={"system_initialized": False, "error": str(e)})

@app.route('/api/search', methods=['POST'])
def api_search():
    """Enhanced search API with hybrid capabilities"""
    try:
        if not hybrid_rag_system or not hybrid_rag_system.is_initialized:
            return jsonify({
                'error': 'System not initialized',
                'success': False
            }), 500
        
        data = request.get_json()
        query = data.get('query', '').strip()
        search_mode = data.get('search_mode', 'comprehensive')
        enable_fact_check = data.get('enable_fact_check', True)
        max_results = data.get('max_results', 10)
        perplexity_enabled = data.get('perplexity_enabled', True)
        
        if not query:
            return jsonify({
                'error': 'Query cannot be empty',
                'success': False
            }), 400
        
        # Adjust search mode if Perplexity is disabled
        if not perplexity_enabled:
            if search_mode == 'perplexity':
                search_mode = 'local'  # Fall back to local search
            elif search_mode == 'comprehensive':
                # Still allow comprehensive but without Perplexity
                pass
            enable_fact_check = False  # Disable fact-checking without Perplexity
        
        logger.info(f"🔍 Processing search query: '{query}' (mode: {search_mode}, perplexity: {perplexity_enabled})")
        
        # Generate comprehensive response
        response = hybrid_rag_system.generate_comprehensive_response(
            query=query,
            search_mode=search_mode,
            perplexity_enabled=perplexity_enabled
        )
        
        # Format response for web interface with enhanced data
        formatted_response = {
            'success': True,
            'query': response.query,
            'ai_response': response.ai_response,
            'search_results': [
                {
                    'content': result.content,
                    'source': result.source,
                    'category': result.category,
                    'relevance_score': result.relevance_score,
                    'metadata': result.metadata,
                    'verification_status': result.verification_status,
                    'misinformation_alert': result.misinformation_alert
                }
                for result in response.search_results
            ],
            'formatted_results': response.formatted_results or [],
            'fact_check_results': response.fact_check_results,
            'misinformation_alerts': response.misinformation_alerts,
            'strategic_advice': response.strategic_advice,
            'sources_used': response.sources_used,
            'confidence_score': response.confidence_score,
            'confidence_recommendation': {
                'current_confidence': response.confidence_recommendation.current_confidence,
                'target_confidence': response.confidence_recommendation.target_confidence,
                'recommended_actions': response.confidence_recommendation.recommended_actions,
                'estimated_improvement': response.confidence_recommendation.estimated_improvement,
                'cost_estimate': response.confidence_recommendation.cost_estimate
            } if response.confidence_recommendation else None,
            'cost_breakdown': response.cost_breakdown,
            'timestamp': response.timestamp
        }
        
        # Store in session for history
        if 'search_history' not in session:
            session['search_history'] = []
        
        session['search_history'].append({
            'query': query,
            'timestamp': response.timestamp,
            'confidence': response.confidence_score,
            'sources': response.sources_used
        })
        
        # Keep only last 10 searches
        session['search_history'] = session['search_history'][-10:]
        
        logger.info(f"✅ Search completed successfully (confidence: {response.confidence_score:.3f})")
        
        return jsonify(formatted_response)
        
    except Exception as e:
        logger.error(f"❌ Error processing search: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': f'Search failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/fact-check', methods=['POST'])
def api_fact_check():
    """Dedicated fact-checking endpoint"""
    try:
        if not hybrid_rag_system or not hybrid_rag_system.is_initialized:
            return jsonify({
                'error': 'System not initialized',
                'success': False
            }), 500
        
        data = request.get_json()
        claim = data.get('claim', '').strip()
        perplexity_enabled = data.get('perplexity_enabled', True)
        
        if not claim:
            return jsonify({
                'error': 'Claim cannot be empty',
                'success': False
            }), 400
        
        if not perplexity_enabled:
            return jsonify({
                'error': 'Fact-checking requires Perplexity API to be enabled',
                'success': False
            }), 400
        
        logger.info(f"🔍 Fact-checking claim: '{claim}'")
        
        # Check cache first
        cached_result = hybrid_rag_system.mcp_memory.get_cached_verification(claim)
        
        if cached_result:
            result = cached_result['result']
            logger.info("✅ Using cached fact-check result")
        else:
            # Perform new fact-check
            result = hybrid_rag_system.perplexity_engine.fact_check_legal_claim(claim)
            hybrid_rag_system.mcp_memory.store_verification_result(claim, result)
            logger.info("✅ New fact-check completed")
        
        return jsonify({
            'success': True,
            'claim': claim,
            'result': result,
            'cached': cached_result is not None,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Error in fact-checking: {e}")
        return jsonify({
            'error': f'Fact-check failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/system-status')
def api_system_status():
    """Get comprehensive system status"""
    try:
        if hybrid_rag_system and hybrid_rag_system.is_initialized:
            status = hybrid_rag_system.get_system_status()
            status['success'] = True
        else:
            status = {
                'success': False,
                'system_initialized': False,
                'error': 'System not initialized'
            }
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"❌ Error getting system status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search-history')
def api_search_history():
    """Get user's search history"""
    try:
        history = session.get('search_history', [])
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        logger.error(f"❌ Error getting search history: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/knowledge-graph')
def api_knowledge_graph():
    """Get knowledge graph data for visualization"""
    try:
        if not hybrid_rag_system or not hybrid_rag_system.is_initialized:
            return jsonify({
                'error': 'System not initialized',
                'success': False
            }), 500
        
        # Get the complete knowledge graph from MCP Memory
        graph_data = hybrid_rag_system.mcp_memory.get_knowledge_graph()
        
        return jsonify({
            'success': True,
            'graph': graph_data
        })
        
    except Exception as e:
        logger.error(f"❌ Error getting knowledge graph: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/delaware-strategy', methods=['POST'])
def api_delaware_strategy():
    """Get Delaware County strategic advice"""
    try:
        if not hybrid_rag_system or not hybrid_rag_system.is_initialized:
            return jsonify({
                'error': 'System not initialized',
                'success': False
            }), 500
        
        data = request.get_json()
        case_type = data.get('case_type', 'divorce')
        query = data.get('query', '').strip()
        perplexity_enabled = data.get('perplexity_enabled', True)
        
        if not query:
            return jsonify({
                'error': 'Query cannot be empty',
                'success': False
            }), 400
        
        if not perplexity_enabled:
            return jsonify({
                'error': 'Delaware County strategy requires Perplexity API to be enabled',
                'success': False
            }), 400
        
        logger.info(f"🏛️ Getting Delaware County strategy for: '{query}'")
        
        strategy_result = hybrid_rag_system.perplexity_engine.research_delaware_county_strategy(
            case_type, query
        )
        
        # Store in knowledge graph
        hybrid_rag_system.mcp_memory.store_delaware_county_intelligence(query, strategy_result)
        
        return jsonify({
            'success': True,
            'query': query,
            'case_type': case_type,
            'strategy': strategy_result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Error getting Delaware strategy: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Enhanced Legal RAG Web Application Starting...")
    
    # Initialize the system
    if initialize_system():
        print("✅ System initialized successfully!")
        print("🌐 Access the enhanced app at: http://localhost:5001")
        print("\n📊 Enhanced Features:")
        print("  • Hybrid search across local documents, Atlas, and Perplexity")
        print("  • Real-time fact-checking with misinformation detection")
        print("  • Delaware County strategic intelligence")
        print("  • Legal knowledge graph with MCP Memory")
        print("  • Pro se protection against legal misinformation")
        print("  • Cost tracking and API usage monitoring")
        
        # Run the Flask app
        app.run(
            host='0.0.0.0',
            port=5001,
            debug=True,
            threaded=True
        )
    else:
        print("❌ Failed to initialize system. Please check the logs.")
        print("💡 Make sure all dependencies are installed and MCP server is running.")