/**
 * Base Court Connector
 * 
 * Abstract base class for connecting to court systems.
 * Jurisdiction-specific connectors should extend this class.
 */
class BaseCourtConnector {
  constructor(options = {}) {
    if (this.constructor === BaseCourtConnector) {
      throw new Error('BaseCourtConnector is abstract and cannot be instantiated directly');
    }
    
    this.options = this._loadConfig(options);
    this.cache = {};
  }
  
  _loadConfig(options) {
    // Default configuration - override in subclasses
    return {
      cacheEnabled: true,
      cacheExpiry: 86400000, // 24 hours
      ...options
    };
  }
  
  // Abstract methods that must be implemented by subclasses
  async searchCases(criteria, jurisdiction) {
    throw new Error('searchCases must be implemented by subclass');
  }
  
  async getJudgeInfo(judgeId, jurisdiction) {
    throw new Error('getJudgeInfo must be implemented by subclass');
  }
  
  async getCourtForms(category, jurisdiction) {
    throw new Error('getCourtForms must be implemented by subclass');
  }
  
  async getFilingRequirements(caseType, jurisdiction) {
    throw new Error('getFilingRequirements must be implemented by subclass');
  }
  
  async getPrecedentCases(issueType, jurisdiction) {
    throw new Error('getPrecedentCases must be implemented by subclass');
  }
  
  // Utility methods that can be used by all subclasses
  _saveToCache(key, data, expiry) {
    if (!this.options.cacheEnabled) return;
    
    this.cache[key] = {
      data,
      timestamp: Date.now(),
      expiry: expiry || Date.now() + this.options.cacheExpiry
    };
  }
  
  _getFromCache(key) {
    if (!this.options.cacheEnabled) return null;
    
    const cached = this.cache[key];
    if (cached && cached.expiry > Date.now()) {
      return cached.data;
    }
    
    return null;
  }
  
  _clearCache() {
    this.cache = {};
  }
  
  _delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = BaseCourtConnector;