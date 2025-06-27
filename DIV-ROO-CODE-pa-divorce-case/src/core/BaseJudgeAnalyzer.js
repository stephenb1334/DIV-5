/**
 * Base Judge Analyzer
 * 
 * Abstract base class for analyzing judge information and ruling patterns.
 * Jurisdiction-specific analyzers should extend this class.
 */
class BaseJudgeAnalyzer {
  constructor(options = {}) {
    if (this.constructor === BaseJudgeAnalyzer) {
      throw new Error('BaseJudgeAnalyzer is abstract and cannot be instantiated directly');
    }
    
    this.options = this._loadConfig(options);
    this.judgeData = {};
    this.courtConnector = options.courtConnector;
  }
  
  _loadConfig(options) {
    // Default configuration - override in subclasses
    return {
      analysisPeriod: 24, // months of data to analyze
      minimumCasesForAnalysis: 10,
      confidenceThreshold: 0.7,
      cacheJudgeData: true,
      cacheExpiry: 7 * 24 * 60 * 60 * 1000, // 1 week
      ...options
    };
  }
  
  // Abstract methods that must be implemented by subclasses
  async getJudgeAnalysis(judgeId, jurisdiction) {
    throw new Error('getJudgeAnalysis must be implemented by subclass');
  }
  
  async findRecommendedJudges(caseInfo, jurisdiction) {
    throw new Error('findRecommendedJudges must be implemented by subclass');
  }
  
  // Shared methods for all judge analyzers
  _calculateConfidenceScore(patterns, caseCount = 0) {
    // Base confidence on number of cases and pattern consistency
    let confidenceScore = 0.5; // Default baseline
    
    if (caseCount) {
      // More cases analyzed = higher confidence, up to a point
      const caseFactor = Math.min(caseCount / 50, 1.0); // Max out at 50 cases
      confidenceScore += caseFactor * 0.3;
    }
    
    // Pattern consistency check
    if (patterns) {
      const values = Object.values(patterns).filter(v => typeof v === 'number');
      if (values.length > 0) {
        // If patterns are extreme (close to 0 or 1), confidence increases
        const avgExtremeValue = values.reduce((sum, val) => {
          return sum + Math.abs(val - 0.5) * 2; // Convert to 0-1 scale
        }, 0) / values.length;
        
        confidenceScore += avgExtremeValue * 0.2;
      }
    }
    
    return Math.min(confidenceScore, 1.0);
  }
  
  _findBestJudgeFor(goal, judgeAnalyses) {
    let bestJudgeId = null;
    let bestScore = -1;
    
    // Map goals to metrics in ruling analysis
    const metricMap = {
      'plaintiff': 'favorPlaintiff',
      'defendant': 'favorDefendant',
      'landlord': 'favorLandlord',
      'tenant': 'favorTenant',
      'settlement': 'settlement',
      'expediency': 'averageCaseLength' // For expediency, lower is better
    };
    
    const metric = metricMap[goal];
    if (!metric) return null;
    
    for (const judgeId in judgeAnalyses) {
      const value = this._extractMetricValue(judgeAnalyses[judgeId], metric);
      
      if (value !== null) {
        if (goal === 'expediency') {
          // For expediency, lower is better
          if (bestScore === -1 || value < bestScore) {
            bestScore = value;
            bestJudgeId = judgeId;
          }
        } else {
          // For other metrics, higher is better
          if (value > bestScore) {
            bestScore = value;
            bestJudgeId = judgeId;
          }
        }
      }
    }
    
    if (bestJudgeId) {
      return {
        id: bestJudgeId,
        name: judgeAnalyses[bestJudgeId].name,
        score: bestScore
      };
    }
    
    return null;
  }
  
  _extractMetricValue(analysis, metric) {
    if (!analysis || !analysis.rulingAnalysis) return null;
    
    // Check different locations in the object structure
    if (analysis.rulingAnalysis.rulingTendencies && 
        analysis.rulingAnalysis.rulingTendencies[metric] !== undefined) {
      return analysis.rulingAnalysis.rulingTendencies[metric];
    }
    
    if (analysis.rulingAnalysis.processTendencies && 
        analysis.rulingAnalysis.processTendencies[metric] !== undefined) {
      return analysis.rulingAnalysis.processTendencies[metric];
    }
    
    if (analysis.statisticalProfile && 
        analysis.statisticalProfile[metric] !== undefined) {
      return analysis.statisticalProfile[metric];
    }
    
    if (analysis.statisticalProfile && 
        analysis.statisticalProfile.rulingPattern &&
        analysis.statisticalProfile.rulingPattern[metric] !== undefined) {
      return analysis.statisticalProfile.rulingPattern[metric];
    }
    
    return null;
  }
  
  _calculateJudgeFitScore(judgeAnalysis, caseInfo) {
    if (!judgeAnalysis.rulingAnalysis) return 50; // Neutral score if no analysis
    
    let score = 50; // Start with neutral score
    const analysis = judgeAnalysis.rulingAnalysis;
    const partyType = caseInfo.partyType;
    
    // Party-specific scoring
    if (partyType === 'tenant' || partyType === 'defendant') {
      // For tenants/defendants, higher tenant/defendant favorability is better
      if (analysis.rulingTendencies.favorTenant !== undefined) {
        score += analysis.rulingTendencies.favorTenant * 40;
        score -= analysis.rulingTendencies.favorLandlord * 30;
      } else if (analysis.rulingTendencies.favorDefendant !== undefined) {
        score += analysis.rulingTendencies.favorDefendant * 40;
        score -= analysis.rulingTendencies.favorPlaintiff * 30;
      }
    } else if (partyType === 'landlord' || partyType === 'plaintiff') {
      // For landlords/plaintiffs, higher landlord/plaintiff favorability is better
      if (analysis.rulingTendencies.favorLandlord !== undefined) {
        score += analysis.rulingTendencies.favorLandlord * 40;
        score -= analysis.rulingTendencies.favorTenant * 30;
      } else if (analysis.rulingTendencies.favorPlaintiff !== undefined) {
        score += analysis.rulingTendencies.favorPlaintiff * 40;
        score -= analysis.rulingTendencies.favorDefendant * 30;
      }
    }
    
    // Adjust for settlement preference if present in case info
    if (caseInfo.preferSettlement) {
      score += analysis.rulingTendencies.settlement * 30;
    }
    
    // Adjust for case complexity
    if (caseInfo.complexity === 'high') {
      // For complex cases, procedural rigidity might be good
      score += (analysis.processTendencies.strictProcedureAdherence - 0.5) * 20;
    }
    
    // Adjust for desired speed
    if (caseInfo.desiredSpeed === 'fast') {
      // Faster cases are better
      score += (1 - analysis.processTendencies.averageCaseLength / 60) * 20; // Normalize to 60 days
    } else if (caseInfo.desiredSpeed === 'slow') {
      // Slower cases are better
      score += (analysis.processTendencies.averageCaseLength / 60) * 20; // Normalize to 60 days
    }
    
    // Clamp score to 0-100 range
    return Math.min(100, Math.max(0, score));
  }
}

module.exports = BaseJudgeAnalyzer;