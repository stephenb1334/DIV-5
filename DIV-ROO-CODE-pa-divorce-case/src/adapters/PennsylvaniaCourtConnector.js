/**
 * Pennsylvania Court Connector
 * 
 * Implementation of the court connector for Pennsylvania courts,
 * specializing in divorce and family law cases.
 */
const BaseCourtConnector = require('../core/BaseCourtConnector');
const fs = require('fs');
const path = require('path');

class PennsylvaniaCourtConnector extends BaseCourtConnector {
  constructor(options = {}) {
    super({
      defaultCounty: 'delaware',
      ...options
    });
    
    this._initializePennsylvaniaCountyData();
  }
  
  _initializePennsylvaniaCountyData() {
    this.countyData = {
      'delaware': {
        name: 'Delaware County',
        baseUrl: 'https://www.co.delaware.pa.us/courts/',
        clerkUrl: 'https://www.co.delaware.pa.us/courts/domesticrelations.html',
        courtScheduleUrl: 'https://www.co.delaware.pa.us/courts/schedule.html',
        formUrl: 'https://www.co.delaware.pa.us/courts/forms/',
        selfHelpUrl: 'https://www.co.delaware.pa.us/courts/selfhelp/',
        courtSystemMap: {
          familyCourt: 'Family Court',
          domesticRelations: 'Domestic Relations',
          orphansCourt: 'Orphans Court'
        },
        localRules: {
          requiresParentingClasses: true,
          requiresDivorceMediationOrientation: true,
          divorceFilingFee: 201.75
        }
      },
      'montgomery': {
        name: 'Montgomery County',
        baseUrl: 'https://www.montcopa.org/1215/Family-Court',
        clerkUrl: 'https://www.montcopa.org/81/Prothonotary',
        formUrl: 'https://www.montcopa.org/204/Forms',
        selfHelpUrl: 'https://www.montcopa.org/1024/Self-Help-Center',
        courtSystemMap: {
          familyCourt: 'Family Court',
          domesticRelations: 'Domestic Relations',
          orphansCourt: 'Orphans Court'
        },
        localRules: {
          requiresParentingClasses: true,
          divorceFilingFee: 206.25
        }
      },
      'chester': {
        name: 'Chester County',
        baseUrl: 'https://www.chesco.org/221/Family-Court',
        clerkUrl: 'https://www.chesco.org/155/Prothonotary',
        formUrl: 'https://www.chesco.org/257/Forms',
        selfHelpUrl: 'https://www.chesco.org/938/Self-Help',
        courtSystemMap: {
          familyCourt: 'Family Court',
          domesticRelations: 'Domestic Relations',
          orphansCourt: 'Register of Wills/Orphans Court'
        },
        localRules: {
          requiresParentingClasses: true,
          divorceFilingFee: 208.50
        }
      }
    };
  }
  
  // Implementation of abstract methods for Pennsylvania
  async searchCases(criteria, county = this.options.defaultCounty) {
    const cacheKey = `searchCases_${county}_${JSON.stringify(criteria)}`;
    const cached = this._getFromCache(cacheKey);
    if (cached) return cached;
    
    // For demo purposes, we'll return mock data
    // In production, this would connect to the Pennsylvania court API
    const mockResults = [
      {
        caseNumber: '2025-000456',
        caseType: 'Divorce',
        filingDate: '2025-04-15',
        status: 'Active',
        parties: [
          { name: 'John Smith', type: 'Plaintiff' },
          { name: 'Jane Smith', type: 'Defendant' }
        ],
        nextHearingDate: '2025-06-30',
        nextHearingType: 'Case Management Conference',
        judge: 'Judge Kimberly Sharpe',
        county: county.toUpperCase()
      },
      {
        caseNumber: '2025-000457',
        caseType: 'Custody',
        filingDate: '2025-04-10',
        status: 'Active',
        parties: [
          { name: 'Michael Johnson', type: 'Plaintiff' },
          { name: 'Susan Johnson', type: 'Defendant' }
        ],
        nextHearingDate: '2025-05-25',
        nextHearingType: 'Conciliation Conference',
        judge: 'Judge Kent Compton',
        county: county.toUpperCase()
      }
    ];
    
    // Filter based on criteria
    const results = mockResults.filter(c => {
      let match = true;
      
      if (criteria.caseType && !c.caseType.toLowerCase().includes(criteria.caseType.toLowerCase())) {
        match = false;
      }
      
      if (criteria.partyName) {
        const hasParty = c.parties.some(p => 
          p.name.toLowerCase().includes(criteria.partyName.toLowerCase()));
        if (!hasParty) match = false;
      }
      
      if (criteria.dateFrom) {
        const fromDate = new Date(criteria.dateFrom);
        const filingDate = new Date(c.filingDate);
        if (filingDate < fromDate) match = false;
      }
      
      return match;
    });
    
    // Add simulated network delay
    await this._delay(500);
    
    // Cache results
    this._saveToCache(cacheKey, results);
    
    return results;
  }
  
  async getJudgeInfo(judgeId, county = this.options.defaultCounty) {
    const cacheKey = `judgeInfo_${county}_${judgeId}`;
    const cached = this._getFromCache(cacheKey);
    if (cached) return cached;
    
    // Mock judge data for Pennsylvania divorce and family court judges
    const judges = {
      'judge-001': {
        id: 'judge-001',
        name: 'Judge Kimberly Sharpe',
        court: 'Delaware County Court of Common Pleas',
        division: 'Family Court',
        appointment: '2016',
        background: 'Former family law attorney with 15 years experience',
        education: 'J.D., Villanova University School of Law',
        statisticalProfile: {
          rulingPattern: {
            favorPlaintiff: 0.47,
            favorDefendant: 0.53,
            settlement: 0.60
          },
          averageCaseLength: 210, // days - divorce cases take longer
          continuanceRate: 0.25
        }
      },
      'judge-002': {
        id: 'judge-002',
        name: 'Judge Kent Compton',
        court: 'Delaware County Court of Common Pleas',
        division: 'Family Court',
        appointment: '2012',
        background: 'Former district attorney',
        education: 'J.D., Temple University',
        statisticalProfile: {
          rulingPattern: {
            favorPlaintiff: 0.52,
            favorDefendant: 0.48,
            settlement: 0.35
          },
          averageCaseLength: 180, // days
          continuanceRate: 0.15
        }
      },
      'judge-003': {
        id: 'judge-003',
        name: 'Judge Martha Wilson',
        court: 'Delaware County Court of Common Pleas',
        division: 'Family Court',
        appointment: '2014',
        background: 'Former family law master',
        education: 'J.D., University of Pennsylvania',
        statisticalProfile: {
          rulingPattern: {
            favorPlaintiff: 0.45,
            favorDefendant: 0.55,
            settlement: 0.70
          },
          averageCaseLength: 195, // days
          continuanceRate: 0.30
        }
      }
    };
    
    // Normalize judge ID
    const normalizedId = judgeId.toLowerCase().replace(/\s+/g, '-');
    
    // Find judge
    let judge = judges[normalizedId] || null;
    
    // If judge not found by ID, try by name
    if (!judge) {
      const judgeByName = Object.values(judges).find(j => 
        j.name.toLowerCase().includes(judgeId.toLowerCase()));
      if (judgeByName) {
        judge = judgeByName;
      }
    }
    
    // If still not found, return basic info
    if (!judge) {
      judge = {
        id: normalizedId,
        name: judgeId,
        court: `${county} County Court of Common Pleas`,
        note: 'Limited information available'
      };
    }
    
    // Add county information
    judge.county = county;
    
    // Add simulated network delay
    await this._delay(300);
    
    // Cache results
    this._saveToCache(cacheKey, judge);
    
    return judge;
  }
  
  async getCourtForms(category, county = this.options.defaultCounty) {
    const cacheKey = `courtForms_${county}_${category}`;
    const cached = this._getFromCache(cacheKey);
    if (cached) return cached;
    
    // Define categories and form mappings for Pennsylvania
    const formCategories = {
      'divorce': [
        {
          id: 'pa-divorce-001',
          name: 'Divorce Complaint',
          description: 'Initial filing to start divorce proceedings',
          url: `https://www.pacourts.us/assets/files/setting-5631/file-5405.pdf`,
          category: 'divorce',
          partyType: 'plaintiff',
          fileType: 'pdf',
          requiresNotarization: true,
          filingFee: 201.75 // Delaware County filing fee
        },
        {
          id: 'pa-divorce-002',
          name: 'Notice to Defend and Claim Rights',
          description: 'Required notice for divorce proceedings',
          url: `https://www.pacourts.us/assets/files/setting-5631/file-5406.pdf`,
          category: 'divorce',
          partyType: 'plaintiff',
          fileType: 'pdf',
          requiresNotarization: false,
          filingFee: 0
        },
        {
          id: 'pa-divorce-003',
          name: 'Verification',
          description: 'Statement verifying truth of complaint allegations',
          url: `https://www.pacourts.us/assets/files/setting-5631/file-5407.pdf`,
          category: 'divorce',
          partyType: 'both',
          fileType: 'pdf',
          requiresNotarization: true,
          filingFee: 0
        },
        {
          id: 'pa-divorce-004',
          name: 'Answer to Divorce Complaint',
          description: 'Response to divorce complaint allegations',
          url: `https://www.pacourts.us/assets/files/setting-5631/file-5408.pdf`,
          category: 'divorce',
          partyType: 'defendant',
          fileType: 'pdf',
          requiresNotarization: true,
          filingFee: 0
        },
        {
          id: 'pa-divorce-005',
          name: 'Counterclaim',
          description: 'Form to file your own claims against plaintiff',
          url: `https://www.pacourts.us/assets/files/setting-5631/file-5409.pdf`,
          category: 'divorce',
          partyType: 'defendant',
          fileType: 'pdf',
          requiresNotarization: true,
          filingFee: 53.48
        },
        {
          id: 'pa-divorce-006',
          name: 'Affidavit of Service',
          description: 'Proof that documents were served on other party',
          url: `https://www.pacourts.us/assets/files/setting-5631/file-5410.pdf`,
          category: 'divorce',
          partyType: 'both',
          fileType: 'pdf',
          requiresNotarization: true,
          filingFee: 0
        },
        {
          id: 'pa-divorce-007',
          name: 'Inventory of Marital Property',
          description: 'Listing of all marital assets and debts',
          url: `https://www.pacourts.us/assets/files/setting-5631/file-5411.pdf`,
          category: 'divorce',
          partyType: 'both',
          fileType: 'pdf',
          requiresNotarization: false,
          filingFee: 0
        }
      ],
      'custody': [
        {
          id: 'pa-custody-001',
          name: 'Custody Complaint',
          description: 'Initial filing to establish custody',
          url: `https://www.pacourts.us/assets/files/setting-5632/file-5415.pdf`,
          category: 'custody',
          partyType: 'plaintiff',
          fileType: 'pdf',
          requiresNotarization: true,
          filingFee: 176.75
        },
        {
          id: 'pa-custody-002',
          name: 'Answer to Custody Complaint',
          description: 'Response to custody complaint',
          url: `https://www.pacourts.us/assets/files/setting-5632/file-5416.pdf`,
          category: 'custody',
          partyType: 'defendant',
          fileType: 'pdf',
          requiresNotarization: true,
          filingFee: 0
        }
      ],
      'support': [
        {
          id: 'pa-support-001',
          name: 'Support Complaint',
          description: 'Petition for child/spousal support',
          url: `https://www.pacourts.us/assets/files/setting-5633/file-5420.pdf`,
          category: 'support',
          partyType: 'plaintiff',
          fileType: 'pdf',
          requiresNotarization: true,
          filingFee: 43.50
        },
        {
          id: 'pa-support-002',
          name: 'Income and Expense Statement',
          description: 'Financial information for support calculations',
          url: `https://www.pacourts.us/assets/files/setting-5633/file-5421.pdf`,
          category: 'support',
          partyType: 'both',
          fileType: 'pdf',
          requiresNotarization: true,
          filingFee: 0
        }
      ]
    };
    
    // Return forms for the requested category
    const forms = formCategories[category] || [];
    
    // Add county-specific information
    const countyForms = forms.map(form => ({
      ...form,
      county,
      countyClerkUrl: this.countyData[county]?.formUrl || null
    }));
    
    // Add simulated network delay
    await this._delay(300);
    
    // Cache results
    this._saveToCache(cacheKey, countyForms);
    
    return countyForms;
  }
  
  async getFilingRequirements(caseType, county = this.options.defaultCounty) {
    const cacheKey = `filingRequirements_${county}_${caseType}`;
    const cached = this._getFromCache(cacheKey);
    if (cached) return cached;
    
    // Define filing requirements by case type for Pennsylvania
    const requirements = {
      'divorce': {
        requiredDocuments: [
          { name: 'Divorce Complaint', description: 'Must include grounds for divorce' },
          { name: 'Notice to Defend and Claim Rights', description: 'Required form notifying defendant of rights' },
          { name: 'Verification', description: 'Sworn statement that complaint is true and correct' },
          { name: 'Civil Cover Sheet', description: 'Pennsylvania Civil Cover Sheet completed and signed' }
        ],
        filingFee: 201.75, // Delaware County filing fee
        filingMethods: [
          { 
            method: 'Online',
            url: `https://pennsylvaniaefile.com`,
            description: 'File through the Pennsylvania electronic filing system'
          },
          { 
            method: 'In Person',
            location: `${county} County Office of Judicial Support`,
            hours: 'Monday-Friday 8:30am-4:30pm',
            description: 'File at the Office of Judicial Support'
          },
          {
            method: 'Mail',
            address: `Office of Judicial Support\n${county} County Courthouse\nMedia, PA 19063`,
            description: 'Send documents and filing fee by mail'
          }
        ],
        specialInstructions: [
          '1. You must have been a resident of Pennsylvania for at least 6 months before filing',
          '2. The notice to defend must be in English and Spanish',
          '3. If you have minor children, you must attend a parenting class within 30 days of filing',
          '4. Provide original plus two copies of all documents',
          '5. Personal service of the complaint is required on the defendant'
        ],
        statutoryReferences: [
          '23 Pa.C.S. § 3301 - Grounds for divorce',
          '23 Pa.C.S. § 3302 - Counseling',
          'Pennsylvania Rules of Civil Procedure 1920 - Actions in Divorce'
        ]
      },
      'custody': {
        requiredDocuments: [
          { name: 'Custody Complaint', description: 'Request for custody order' },
          { name: 'Verification', description: 'Sworn statement that complaint is true and correct' },
          { name: 'Criminal Record/Abuse History Verification', description: 'Required disclosure of criminal/abuse history' },
          { name: 'Civil Cover Sheet', description: 'Pennsylvania Civil Cover Sheet completed and signed' }
        ],
        filingFee: 176.75,
        filingMethods: [
          { 
            method: 'Online',
            url: `https://pennsylvaniaefile.com`,
            description: 'File through the Pennsylvania electronic filing system'
          },
          { 
            method: 'In Person',
            location: `${county} County Office of Judicial Support`,
            hours: 'Monday-Friday 8:30am-4:30pm',
            description: 'File at the Office of Judicial Support'
          }
        ],
        specialInstructions: [
          '1. You must attend a custody education seminar within 30 days of filing',
          '2. You must attend custody mediation/conciliation',
          '3. Criminal Record/Abuse History Verification is mandatory',
          '4. The court may order a custody evaluation'
        ],
        statutoryReferences: [
          '23 Pa.C.S. § 5321-5340 - Child Custody',
          'Pennsylvania Rules of Civil Procedure 1915 - Actions for Custody'
        ]
      },
      'support': {
        requiredDocuments: [
          { name: 'Support Complaint', description: 'Request for child or spousal support' },
          { name: 'Income and Expense Statement', description: 'Detailed financial information' },
          { name: 'Six months of pay stubs/income verification', description: 'Proof of income' },
          { name: 'Most recent tax return', description: 'Federal tax return with all schedules' }
        ],
        filingFee: 43.50,
        filingMethods: [
          { 
            method: 'In Person',
            location: `${county} County Domestic Relations Section`,
            hours: 'Monday-Friday 8:30am-4:30pm',
            description: 'File at the Domestic Relations Section'
          }
        ],
        specialInstructions: [
          '1. A support conference will be scheduled automatically',
          '2. Bring proof of expenses to the support conference',
          '3. Support is calculated using the Pennsylvania Support Guidelines'
        ],
        statutoryReferences: [
          '23 Pa.C.S. § 4301-4353 - Support Matters',
          'Pennsylvania Rules of Civil Procedure 1910 - Actions for Support'
        ]
      }
    };
    
    // Get requirements for the specified case type
    const result = requirements[caseType] || {
      requiredDocuments: [],
      filingFee: 0,
      filingMethods: [],
      specialInstructions: ['Information not available for this case type.'],
      statutoryReferences: []
    };
    
    // Add county-specific information
    result.county = county;
    result.countyClerkUrl = this.countyData[county]?.clerkUrl || null;
    if (this.countyData[county]?.localRules) {
      result.localRules = this.countyData[county].localRules;
    }
    
    // Add simulated network delay
    await this._delay(300);
    
    // Cache results
    this._saveToCache(cacheKey, result);
    
    return result;
  }
  
  async getPrecedentCases(issueType, county = this.options.defaultCounty) {
    const cacheKey = `precedentCases_${county}_${issueType}`;
    const cached = this._getFromCache(cacheKey);
    if (cached) return cached;
    
    // Define precedent cases by issue type for Pennsylvania
    const precedents = {
      'divorce': [
        {
          id: 'pa-prec-001',
          caseName: 'Litmans v. Litmans',
          citation: '449 Pa. Super. 209 (1996)',
          summary: 'Established standards for equitable distribution of marital property',
          statutes: ['23 Pa.C.S. § 3502'],
          holding: 'Court must consider all relevant factors when distributing marital property'
        },
        {
          id: 'pa-prec-002',
          caseName: 'Teodorski v. Teodorski',
          citation: '857 A.2d 194 (Pa. Super. 2004)',
          summary: 'Addresses valuation date for marital assets',
          statutes: ['23 Pa.C.S. § 3501'],
          holding: 'Assets should generally be valued as close to distribution as practicable'
        },
        {
          id: 'pa-prec-003',
          caseName: 'Smith v. Smith',
          citation: '904 A.2d 15 (Pa. Super. 2006)',
          summary: 'Addresses alimony determination factors',
          statutes: ['23 Pa.C.S. § 3701'],
          holding: 'Court must consider all 17 statutory factors when determining alimony'
        }
      ],
      'custody': [
        {
          id: 'pa-prec-004',
          caseName: 'D.K. v. S.P.K.',
          citation: '102 A.3d 467 (Pa. Super. 2014)',
          summary: 'Addresses relocation in custody cases',
          statutes: ['23 Pa.C.S. § 5337'],
          holding: 'Court must consider 10 relocation factors and 16 custody factors'
        },
        {
          id: 'pa-prec-005',
          caseName: 'C.R.F. v. S.E.F.',
          citation: '45 A.3d 441 (Pa. Super. 2012)',
          summary: 'Addresses custody evaluation findings',
          statutes: ['23 Pa.C.S. § 5328'],
          holding: 'Court cannot delegate decision-making authority to custody evaluator'
        }
      ],
      'support': [
        {
          id: 'pa-prec-006',
          caseName: 'Hanrahan v. Bakker',
          citation: '186 A.3d 958 (Pa. 2018)',
          summary: 'Addresses determination of income for high-income support cases',
          statutes: ['Pa.R.C.P. 1910.16-2'],
          holding: 'Courts must carefully analyze reasonable needs when calculating support in high-income cases'
        }
      ]
    };
    
    // Get precedent cases for the specified issue
    const result = precedents[issueType] || [];
    
    // Add simulated network delay
    await this._delay(500);
    
    // Cache results
    this._saveToCache(cacheKey, result);
    
    return result;
  }
}

module.exports = PennsylvaniaCourtConnector;