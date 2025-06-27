/**
 * Core Legal Framework Components
 * 
 * This module exports abstract base classes for building
 * jurisdiction-specific legal case management systems.
 * 
 * These base classes provide core functionality while allowing
 * jurisdiction-specific implementations to customize behavior
 * for different legal systems.
 */

const BaseCourtConnector = require('./BaseCourtConnector');
const BaseCasePlanner = require('./BaseCasePlanner');
const BaseJudgeAnalyzer = require('./BaseJudgeAnalyzer');
const BaseTimelineGenerator = require('./BaseTimelineGenerator');

/**
 * Create a base legal system
 * @param {Object} options - Configuration options
 * @returns {Object} - Configured components
 */
function createBase(options = {}) {
  const connector = options.connector;
  const planner = options.planner;
  const analyzer = options.analyzer;
  const generator = options.generator;
  
  if (!connector || !planner || !analyzer || !generator) {
    throw new Error('Cannot create base legal system without concrete implementations of all components');
  }
  
  return {
    connector,
    planner,
    analyzer,
    generator,
    
    // Base methods
    async getJudgeAnalysis(judgeId, jurisdiction) {
      return await analyzer.getJudgeAnalysis(judgeId, jurisdiction);
    },
    
    async generateActionPlan(caseInfo, options = {}) {
      return await planner.generateActionPlan(caseInfo, options);
    },
    
    async generateTimeline(caseInfo, options = {}) {
      return await generator.generateTimeline(caseInfo, options);
    },
    
    async generateFormsPackage(caseInfo, jurisdiction) {
      return await generator.generateFormsPackage(caseInfo, jurisdiction);
    }
  };
}

module.exports = {
  BaseCourtConnector,
  BaseCasePlanner,
  BaseJudgeAnalyzer,
  BaseTimelineGenerator,
  createBase
};