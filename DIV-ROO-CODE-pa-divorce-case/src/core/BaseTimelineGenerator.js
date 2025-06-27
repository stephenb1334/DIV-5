/**
 * Base Timeline Generator
 * 
 * Abstract base class for generating visual timelines and calendars.
 * Jurisdiction-specific generators can extend this class.
 */
class BaseTimelineGenerator {
  constructor(options = {}) {
    if (this.constructor === BaseTimelineGenerator) {
      throw new Error('BaseTimelineGenerator is abstract and cannot be instantiated directly');
    }
    
    this.options = this._loadConfig(options);
    this.courtConnector = options.courtConnector;
    this.casePlanner = options.casePlanner;
    this.judgeAnalyzer = options.judgeAnalyzer;
  }
  
  _loadConfig(options) {
    // Default configuration - override in subclasses
    return {
      addSafetyBuffers: true,
      bufferDays: 2,
      includeWeekends: false,
      outputFormats: ['json', 'html'],
      autoAddCriticalDateReminders: true,
      reminderDays: [7, 3, 1],
      includeJudgeInfo: true,
      includeRiskAssessment: true,
      strategicInformation: true,
      mergeSimilarEvents: true,
      colorCodeByPriority: true,
      ...options
    };
  }
  
  // Abstract methods that must be implemented by subclasses
  async generateTimeline(caseInfo, options) {
    throw new Error('generateTimeline must be implemented by subclass');
  }
  
  async generateFormsPackage(caseInfo, jurisdiction) {
    throw new Error('generateFormsPackage must be implemented by subclass');
  }
  
  // Shared timeline generation methods
  _addSafetyBuffers(timeline, bufferDays) {
    // For each phase
    for (const phase of timeline.phases) {
      // For each event
      for (const event of phase.events) {
        // Only add buffer to deadlines and filings
        if (['legal_deadline', 'filing'].includes(event.type)) {
          const date = new Date(event.date);
          date.setDate(date.getDate() - bufferDays);
          event.originalDate = event.date; // Save original date
          event.date = date.toISOString().split('T')[0];
          event.hasBuffer = true;
          event.bufferDays = bufferDays;
        }
      }
    }
    
    // Also adjust key deadlines
    if (timeline.keyDeadlines) {
      for (const deadline of timeline.keyDeadlines) {
        const date = new Date(deadline.date);
        date.setDate(date.getDate() - bufferDays);
        deadline.originalDate = deadline.date; // Save original date
        deadline.date = date.toISOString().split('T')[0];
        deadline.hasBuffer = true;
        deadline.bufferDays = bufferDays;
      }
    }
    
    return timeline;
  }
  
  _addReminderEvents(timeline, reminderDays) {
    // For each phase
    for (const phase of timeline.phases) {
      const reminders = [];
      
      // For each event
      for (const event of phase.events) {
        // Only add reminders to high priority events
        if (event.priority === 'high') {
          for (const days of reminderDays) {
            const originalDate = event.originalDate || event.date;
            const date = new Date(originalDate);
            date.setDate(date.getDate() - days);
            const reminderDate = date.toISOString().split('T')[0];
            
            // Check if the reminder is in the future
            if (new Date(reminderDate) > new Date()) {
              reminders.push({
                id: `reminder-${event.id}-${days}`,
                title: `Reminder: ${event.title}`,
                description: `Reminder for upcoming deadline: ${event.title}`,
                date: reminderDate,
                type: 'reminder',
                priority: 'medium',
                relatedEventId: event.id,
                daysBeforeDeadline: days,
                status: 'pending'
              });
            }
          }
        }
      }
      
      // Add reminders to events
      phase.events = [...phase.events, ...reminders];
      
      // Sort events by date
      phase.events.sort((a, b) => new Date(a.date) - new Date(b.date));
    }
    
    return timeline;
  }
  
  _generateRiskAssessment(timeline, caseInfo) {
    const riskFactors = [];
    let overallRisk = 'low';
    
    // Check for tight deadlines
    let tightDeadlineCount = 0;
    let criticalDeadlines = [];
    
    for (const phase of timeline.phases) {
      for (const event of phase.events) {
        if (event.priority === 'high') {
          // Calculate days until deadline
          const deadlineDate = new Date(event.date);
          const today = new Date();
          const daysUntil = Math.ceil((deadlineDate - today) / (1000 * 60 * 60 * 24));
          
          if (daysUntil < 7 && daysUntil > 0) {
            tightDeadlineCount++;
            criticalDeadlines.push({
              title: event.title,
              date: event.date,
              daysRemaining: daysUntil
            });
          }
        }
      }
    }
    
    if (tightDeadlineCount > 0) {
      riskFactors.push({
        type: 'tight_deadlines',
        severity: tightDeadlineCount > 2 ? 'high' : 'medium',
        description: `${tightDeadlineCount} critical deadline(s) within the next 7 days`,
        details: criticalDeadlines
      });
    }
    
    // Check for complexity risks
    if (caseInfo.complexity === 'high') {
      riskFactors.push({
        type: 'case_complexity',
        severity: 'high',
        description: 'High complexity case may require additional preparation time',
        details: {
          recommendation: 'Consider consulting with an attorney for complex legal aspects'
        }
      });
    }
    
    // Check for judge-related risks
    if (timeline.judgeInfo && timeline.judgeInfo.rulingAnalysis) {
      const analysis = timeline.judgeInfo.rulingAnalysis;
      const partyType = caseInfo.partyType;
      
      this._addJudgeRelatedRisks(riskFactors, analysis, partyType);
    }
    
    // Determine overall risk
    if (riskFactors.some(r => r.severity === 'high')) {
      overallRisk = 'high';
    } else if (riskFactors.some(r => r.severity === 'medium')) {
      overallRisk = 'medium';
    }
    
    return {
      overallRisk,
      riskFactors,
      mitigationStrategies: this._generateRiskMitigationStrategies(riskFactors, caseInfo)
    };
  }
  
  _addJudgeRelatedRisks(riskFactors, analysis, partyType) {
    // This method should be overridden by jurisdiction-specific subclasses
    // to add appropriate judge-related risks
    
    // Generic risk factor for procedural strictness
    if (analysis.processTendencies && analysis.processTendencies.strictProcedureAdherence > 0.7) {
      riskFactors.push({
        type: 'procedural_strictness',
        severity: 'medium',
        description: 'Judge strictly enforces procedural requirements',
        details: {
          strictnessScore: analysis.processTendencies.strictProcedureAdherence,
          recommendation: 'Double-check all filing requirements and deadlines'
        }
      });
    }
  }
  
  _generateRiskMitigationStrategies(riskFactors, caseInfo) {
    const strategies = [];
    
    for (const risk of riskFactors) {
      switch (risk.type) {
        case 'tight_deadlines':
          strategies.push({
            risk: risk.type,
            strategy: 'Prioritize immediate attention to upcoming deadlines',
            actions: [
              'Block dedicated time in your calendar for each critical deadline',
              'Prepare documents at least 2 days before filing deadlines',
              'Set up multiple reminders for each deadline'
            ]
          });
          break;
        
        case 'procedural_strictness':
          strategies.push({
            risk: risk.type,
            strategy: 'Ensure meticulous compliance with court procedures',
            actions: [
              'Double-check all court filing requirements',
              'Review local court rules for any special requirements',
              'Use court-approved forms whenever available',
              'Consider consulting with an attorney to review filings'
            ]
          });
          break;
        
        case 'case_complexity':
          strategies.push({
            risk: risk.type,
            strategy: 'Simplify complex issues for presentation',
            actions: [
              'Create a clear timeline of key events',
              'Prepare a concise summary of main legal issues',
              'Organize evidence into clearly labeled categories',
              'Consider consulting with an attorney for complex aspects'
            ]
          });
          break;
      }
    }
    
    // Add general strategies
    strategies.push({
      risk: 'general',
      strategy: 'General case preparation best practices',
      actions: [
        'Organize all documents in a labeled binder or folder',
        'Make multiple copies of all evidence and filings',
        'Practice explaining your case in clear, concise language',
        'Arrive at court at least 30 minutes before scheduled hearings'
      ]
    });
    
    return strategies;
  }
  
  // Output format generators
  async generateVisualization(timeline, format = 'json') {
    try {
      switch (format.toLowerCase()) {
        case 'html':
          return this._generateHtmlVisualization(timeline);
        case 'csv':
          return this._generateCsvVisualization(timeline);
        case 'json':
        default:
          return JSON.stringify(timeline, null, 2);
      }
    } catch (error) {
      console.error('Error generating visualization:', error);
      throw error;
    }
  }
  
  async generateCalendar(timeline, format = 'json') {
    try {
      const events = this._extractCalendarEvents(timeline);
      
      switch (format.toLowerCase()) {
        case 'ical':
          return this._generateICalCalendar(events);
        case 'json':
        default:
          return JSON.stringify(events, null, 2);
      }
    } catch (error) {
      console.error('Error generating calendar:', error);
      throw error;
    }
  }
  
  _extractCalendarEvents(timeline) {
    const events = [];
    
    // For each phase
    for (const phase of timeline.phases) {
      // For each event
      for (const event of phase.events) {
        // Skip reminder events (they are generated separately in calendars)
        if (event.type === 'reminder') continue;
        
        // Only include high and medium priority events
        if (['high', 'medium'].includes(event.priority)) {
          events.push({
            id: event.id,
            title: event.title,
            description: event.description,
            start: `${event.date}T09:00:00`,
            end: `${event.date}T10:00:00`,
            allDay: false,
            priority: event.priority,
            type: event.type,
            phase: phase.name
          });
        }
      }
    }
    
    return events;
  }
  
  _generateHtmlVisualization(timeline) {
    // This should be overridden by subclasses to provide jurisdiction-specific
    // HTML visualizations. Here we provide a minimal implementation.
    
    return `<!DOCTYPE html>
<html>
<head>
  <title>${timeline.title || "Legal Case Timeline"}</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    h1, h2 { color: #333; }
    .timeline { border: 1px solid #ccc; padding: 20px; }
    .phase { margin-bottom: 20px; }
    .event { margin: 10px 0; padding: 10px; border-left: 4px solid #333; }
    .high { border-left-color: #ff0000; }
    .medium { border-left-color: #ffaa00; }
    .low { border-left-color: #00aa00; }
  </style>
</head>
<body>
  <h1>${timeline.title || "Legal Case Timeline"}</h1>
  <div class="timeline">
    ${this._generateHtmlTimelineContent(timeline)}
  </div>
</body>
</html>`;
  }
  
  _generateHtmlTimelineContent(timeline) {
    let html = '';
    
    // Generate phases and events
    for (const phase of timeline.phases || []) {
      html += `<div class="phase">
        <h2>${phase.name}</h2>
        <p>${phase.description || ''}</p>
        <p><strong>From:</strong> ${phase.startDate} <strong>To:</strong> ${phase.endDate}</p>`;
      
      // Generate events
      for (const event of phase.events || []) {
        html += `<div class="event ${event.priority}">
          <h3>${event.title}</h3>
          <p><strong>Date:</strong> ${event.date}</p>
          <p><strong>Type:</strong> ${event.type}</p>
          <p>${event.description || ''}</p>
        </div>`;
      }
      
      html += '</div>';
    }
    
    return html;
  }
  
  _generateCsvVisualization(timeline) {
    let csv = 'Date,Phase,Event,Type,Priority,Description\n';
    
    // For each phase
    for (const phase of timeline.phases || []) {
      // For each event
      for (const event of phase.events || []) {
        // Escape fields for CSV
        const eventDate = event.date;
        const phaseName = this._escapeCSV(phase.name);
        const eventTitle = this._escapeCSV(event.title);
        const eventType = this._escapeCSV(event.type);
        const eventPriority = this._escapeCSV(event.priority);
        const eventDesc = this._escapeCSV(event.description || '');
        
        csv += `${eventDate},${phaseName},${eventTitle},${eventType},${eventPriority},${eventDesc}\n`;
      }
    }
    
    return csv;
  }
  
  _generateICalCalendar(events) {
    let ical = 'BEGIN:VCALENDAR\r\n';
    ical += 'VERSION:2.0\r\n';
    ical += 'PRODID:-//Legal Case Framework//Timeline Generator//EN\r\n';
    ical += 'CALSCALE:GREGORIAN\r\n';
    ical += 'METHOD:PUBLISH\r\n';
    
    // For each event
    for (const event of events || []) {
      // Format dates for iCal
      const startDate = event.start.replace(/[-:]/g, '');
      const endDate = event.end.replace(/[-:]/g, '');
      
      ical += 'BEGIN:VEVENT\r\n';
      ical += `UID:${event.id}\r\n`;
      ical += `DTSTAMP:${this._formatDateForICal(new Date())}\r\n`;
      ical += `DTSTART:${startDate}\r\n`;
      ical += `DTEND:${endDate}\r\n`;
      ical += `SUMMARY:${event.title}\r\n`;
      ical += `DESCRIPTION:${(event.description || '').replace(/\n/g, '\\n')}\r\n`;
      
      // Add priority
      let priority = 5;
      if (event.priority === 'high') priority = 1;
      else if (event.priority === 'medium') priority = 5;
      else if (event.priority === 'low') priority = 9;
      
      ical += `PRIORITY:${priority}\r\n`;
      
      // Add alarm for high priority events
      if (event.priority === 'high') {
        ical += 'BEGIN:VALARM\r\n';
        ical += 'ACTION:DISPLAY\r\n';
        ical += 'DESCRIPTION:Reminder\r\n';
        ical += 'TRIGGER:-P1D\r\n'; // 1 day before
        ical += 'END:VALARM\r\n';
      }
      
      ical += 'END:VEVENT\r\n';
    }
    
    ical += 'END:VCALENDAR\r\n';
    
    return ical;
  }
  
  _formatDateForICal(date) {
    const pad = (n) => n < 10 ? `0${n}` : n;
    
    return `${date.getUTCFullYear()}${pad(date.getUTCMonth() + 1)}${pad(date.getUTCDate())}T${pad(date.getUTCHours())}${pad(date.getUTCMinutes())}${pad(date.getUTCSeconds())}Z`;
  }
  
  _escapeCSV(str) {
    if (typeof str !== 'string') return '';
    
    // If string contains comma, quote, or newline, wrap in quotes and escape quotes
    if (str.includes(',') || str.includes('"') || str.includes('\n')) {
      return `"${str.replace(/"/g, '""')}"`;
    }
    
    return str;
  }
  
  _capitalize(str) {
    if (typeof str !== 'string' || !str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
  }
}

module.exports = BaseTimelineGenerator;