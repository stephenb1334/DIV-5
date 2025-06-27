/**
 * Base Case Planner
 * 
 * Abstract base class for generating case action plans.
 * Jurisdiction-specific planners should extend this class.
 */
class BaseCasePlanner {
  constructor(options = {}) {
    if (this.constructor === BaseCasePlanner) {
      throw new Error('BaseCasePlanner is abstract and cannot be instantiated directly');
    }
    
    this.options = this._loadConfig(options);
    this.timelineTemplates = {};
    this.courtConnector = options.courtConnector;
  }
  
  _loadConfig(options) {
    // Default configuration - override in subclasses
    return {
      includeDeadlineReminders: true,
      reminderOffsetDays: 3,
      conservativeTimelineEstimates: true,
      includeCalendarEvents: true,
      includeProcedureDetails: true,
      ...options
    };
  }
  
  // Abstract methods that must be implemented by subclasses
  async generateActionPlan(caseInfo, options) {
    throw new Error('generateActionPlan must be implemented by subclass');
  }
  
  // Shared methods for all case planners
  _calculateTotalHours(timeline) {
    let totalHours = 0;
    
    // Sum up all step hours across all phases
    for (const phase of timeline.phases) {
      for (const step of phase.steps) {
        totalHours += step.estimated_hours || 0;
      }
    }
    
    return totalHours;
  }
  
  _calculateTotalCost(timeline, hourlyRate = 150) {
    const totalHours = this._calculateTotalHours(timeline);
    return totalHours * hourlyRate;
  }
  
  _extractKeyDeadlines(timeline) {
    const deadlines = [];
    
    // Extract critical deadlines from all phases
    for (const phase of timeline.phases) {
      for (const step of phase.steps) {
        if (['statutory', 'court_scheduled', 'filing_deadline'].includes(step.deadline_type)) {
          deadlines.push({
            name: step.name,
            description: step.description,
            date: step.deadlineDate,
            phase: phase.name,
            type: step.deadline_type,
            criticalPath: true
          });
        }
      }
    }
    
    // Sort deadlines by date
    deadlines.sort((a, b) => new Date(a.date) - new Date(b.date));
    
    return deadlines;
  }
  
  _calculateDeadlineDate(startDate, daysOffset, daysType = 'calendar') {
    const start = new Date(startDate);
    
    if (daysType === 'business') {
      return this._addBusinessDays(start, daysOffset);
    } else {
      // Calendar days
      const result = new Date(start);
      result.setDate(result.getDate() + daysOffset);
      return result.toISOString().split('T')[0];
    }
  }
  
  _addBusinessDays(startDate, days) {
    const date = new Date(startDate);
    let daysAdded = 0;
    
    while (daysAdded < days) {
      date.setDate(date.getDate() + 1);
      const dayOfWeek = date.getDay();
      if (dayOfWeek !== 0 && dayOfWeek !== 6) {
        // Not a weekend day
        daysAdded++;
      }
    }
    
    return date.toISOString().split('T')[0];
  }
  
  _calculatePriority(step) {
    // Priority calculation logic shared across jurisdictions
    const highPriorityTypes = ['statutory', 'court_scheduled', 'filing_deadline', 'immediate'];
    const mediumPriorityTypes = ['pre_trial', 'strategic', 'pre_hearing'];
    
    if (highPriorityTypes.includes(step.deadline_type)) {
      return 'high';
    } else if (mediumPriorityTypes.includes(step.deadline_type)) {
      return 'medium';
    }
    
    return 'low';
  }
  
  _applyTimeframeToPhase(phase, startDate, phaseEndCallback = null) {
    const newPhase = { ...phase };
    let currentDate = startDate;
    
    // If phase has a specified timeframe like "3-5 days"
    if (phase.timeframe && typeof phase.timeframe === 'string') {
      const match = phase.timeframe.match(/(\d+)\s*-\s*(\d+)\s*days?/i);
      if (match) {
        const minDays = parseInt(match[1], 10);
        const maxDays = parseInt(match[2], 10);
        const days = this.options.conservativeTimelineEstimates ? maxDays : minDays;
        
        // Calculate end date for phase
        const endDate = new Date(startDate);
        endDate.setDate(endDate.getDate() + days);
        
        newPhase.startDate = startDate;
        newPhase.endDate = endDate.toISOString().split('T')[0];
        
        // Distribute steps within the phase duration
        if (newPhase.steps && newPhase.steps.length > 0) {
          const stepCount = newPhase.steps.length;
          const daysPerStep = Math.max(1, Math.floor(days / stepCount));
          
          newPhase.steps = newPhase.steps.map((step, index) => {
            const stepDate = new Date(startDate);
            stepDate.setDate(stepDate.getDate() + (index * daysPerStep));
            
            return {
              ...step,
              deadlineDate: stepDate.toISOString().split('T')[0]
            };
          });
        }
        
        currentDate = newPhase.endDate;
      }
    } else {
      // Apply specific deadlines to each step
      if (newPhase.steps && newPhase.steps.length > 0) {
        let phaseEndDate = new Date(startDate);
        
        newPhase.steps = newPhase.steps.map(step => {
          let deadlineDate;
          
          if (step.deadline_days !== undefined) {
            deadlineDate = this._calculateDeadlineDate(
              startDate,
              step.deadline_days,
              step.deadline_days_type || 'calendar'
            );
            
            const stepEndDate = new Date(deadlineDate);
            if (stepEndDate > phaseEndDate) {
              phaseEndDate = stepEndDate;
            }
          }
          
          return {
            ...step,
            deadlineDate: deadlineDate || startDate
          };
        });
        
        newPhase.startDate = startDate;
        newPhase.endDate = phaseEndDate.toISOString().split('T')[0];
        
        currentDate = newPhase.endDate;
      }
    }
    
    // Call the callback if provided
    if (phaseEndCallback && typeof phaseEndCallback === 'function') {
      phaseEndCallback(currentDate);
    }
    
    return { phase: newPhase, nextStartDate: currentDate };
  }
  
  _generateStrategicRecommendations(caseInfo, timeline) {
    // Base recommendations shared across all jurisdictions
    const recommendations = [
      {
        type: "general",
        title: "Documentation Organization",
        recommendation: "Maintain all documents in a well-organized folder with clear naming conventions.",
        priority: "medium"
      },
      {
        type: "communication",
        title: "Written Communication",
        recommendation: "Always communicate in writing and keep copies of all correspondence.",
        priority: "high"
      },
      {
        type: "preparation",
        title: "Court Appearance",
        recommendation: "Arrive 30 minutes early for all court appearances with all necessary documentation.",
        priority: "high"
      }
    ];
    
    return recommendations;
  }
}

module.exports = BaseCasePlanner;