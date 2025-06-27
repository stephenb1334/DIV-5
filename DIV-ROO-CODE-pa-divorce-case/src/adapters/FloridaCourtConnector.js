/**
 * Florida Court Connector
 * 
 * Implementation of the court connector for Florida courts,
 * specializing in landlord-tenant cases.
 */
const BaseCourtConnector = require('../core/BaseCourtConnector');
const fs = require('fs');
const path = require('path');

class FloridaCourtConnector extends BaseCourtConnector {
  constructor(options = {}) {
    super({
      defaultCounty: 'pinellas',
      ...options
    });
    
    this._initializeFloridaCountyData();
  }
  
  _initializeFloridaCountyData() {
    this.countyData = {
      'pinellas': {
        name: 'Pinellas County',
        baseUrl: 'https://ccmspa.pinellascounty.org',
        clerkUrl: 'https://www.mypinellasclerk.org',
        courtScheduleUrl: 'https://www.mypinellasclerk.org/Home/Court-Calendars',
        formUrl: 'https://www.mypinellasclerk.org/Home/Forms',
        selfHelpUrl: 'https://www.mypinellasclerk.org/Home/Self-Help-Center',
        courtSystemMap: {
          county: 'Pinellas County Court',
          circuit: 'Sixth Judicial Circuit'
        },
        localRules: {
          requiresMediation: true,
          evictionFilingFee: 185.00
        }
      },
      'hillsborough': {
        name: 'Hillsborough County',
        baseUrl: 'https://www.hillsclerk.com',
        clerkUrl: 'https://www.hillsclerk.com',
        courtScheduleUrl: 'https://www.hillsclerk.com/Court-Services/Court-Calendars',
        formUrl: 'https://www.hillsclerk.com/Court-Services/Forms',
        selfHelpUrl: 'https://www.hillsclerk.com/Court-Services/Self-Help',
        courtSystemMap: {
          county: 'Hillsborough County Court',
          circuit: 'Thirteenth Judicial Circuit'
        },
        localRules: {
          requiresMediation: true,
          evictionFilingFee: 185.00
        }
      },
      'pasco': {
        name: 'Pasco County',
        baseUrl: 'https://www.pascoclerk.com',
        clerkUrl: 'https://www.pascoclerk.com',
        formUrl: 'https://www.pascoclerk.com/services/forms',
        courtSystemMap: {
          county: 'Pasco County Court',
          circuit: 'Sixth Judicial Circuit'
        },
        localRules: {
          requiresMediation: true,
          evictionFilingFee: 185.00
        }
      }
    };
  }
  
  // Implementation of abstract methods for Florida
  async searchCases(criteria, county = this.options.defaultCounty) {
    const cacheKey = `searchCases_${county}_${JSON.stringify(criteria)}`;
    const cached = this._getFromCache(cacheKey);
    if (cached) return cached;
    
    // For demo purposes, we'll return mock data
    // In production, this would connect to the Florida court API
    const mockResults = [
      {
        caseNumber: '2025-12345-SC',
        caseType: 'Eviction',
        filingDate: '2025-04-15',
        status: 'Active',
        parties: [
          { name: 'John Smith', type: 'Plaintiff', role: 'Landlord' },
          { name: 'Jane Doe', type: 'Defendant', role: 'Tenant' }
        ],
        nextHearingDate: '2025-05-30',
        nextHearingType: 'Initial Hearing',
        judge: 'Judge Thomas Minkoff',
        county: county.toUpperCase()
      },
      {
        caseNumber: '2025-12346-SC',
        caseType: 'Small Claims',
        filingDate: '2025-04-01',
        status: 'Active',
        parties: [
          { name: 'Property Management Inc.', type: 'Plaintiff', role: 'Landlord' },
          { name: 'Bob Johnson', type: 'Defendant', role: 'Tenant' }
        ],
        nextHearingDate: '2025-05-25',
        nextHearingType: 'Pre-trial Conference',
        judge: 'Judge Dorothy Vaccaro',
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
    
    // Mock judge data
    const judges = {
      'judge-001': {
        id: 'judge-001',
        name: 'Judge Thomas Minkoff',
        court: 'Pinellas County Court',
        division: 'Civil',
        appointment: '2010',
        background: 'Former private practice attorney specializing in real estate law',
        education: 'J.D., University of Florida',
        statisticalProfile: {
          landlordTenantRulingPattern: {
            favorLandlord: 0.65,
            favorTenant: 0.35,
            settlement: 0.25
          },
          averageCaseLength: 42, // days
          continuanceRate: 0.15
        }
      },
      'judge-002': {
        id: 'judge-002',
        name: 'Judge Cynthia Newton',
        court: 'Pinellas County Court',
        division: 'Civil',
        appointment: '2015',
        background: 'Former public defender',
        education: 'J.D., Florida State University',
        statisticalProfile: {
          landlordTenantRulingPattern: {
            favorLandlord: 0.45,
            favorTenant: 0.55,
            settlement: 0.35
          },
          averageCaseLength: 38, // days
          continuanceRate: 0.25
        }
      },
      'judge-003': {
        id: 'judge-003',
        name: 'Judge Lorraine Kelly',
        court: 'Pinellas County Court',
        division: 'Civil',
        appointment: '2012',
        background: 'Former prosecutor and private practice',
        education: 'J.D., Stetson University',
        statisticalProfile: {
          landlordTenantRulingPattern: {
            favorLandlord: 0.55,
            favorTenant: 0.45,
            settlement: 0.15
          },
          averageCaseLength: 35, // days
          continuanceRate: 0.10
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
        court: `${county} County Court`,
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
    
    // Define categories and form mappings
    const formCategories = {
      'eviction': [
        {
          id: 'fl-eviction-001',
          name: 'Complaint for Eviction',
          description: 'Initial filing to begin eviction proceedings',
          url: `https://www.flcourts.org/content/download/404307/file/form_0034_eviction_complaint.pdf`,
          category: 'eviction',
          partyType: 'landlord',
          fileType: 'pdf',
          filingFee: 185.00
        },
        {
          id: 'fl-eviction-002',
          name: 'Summons - Eviction Claim',
          description: 'Summons to be served with eviction complaint',
          url: `https://www.flcourts.org/content/download/404309/file/form_0037_summons_eviction_claim.pdf`,
          category: 'eviction',
          partyType: 'landlord',
          fileType: 'pdf',
          filingFee: 0
        },
        {
          id: 'fl-eviction-003',
          name: 'Answer to Eviction Complaint',
          description: 'Form for tenant to respond to eviction complaint',
          url: `https://www.flcourts.org/content/download/404311/file/form_0038_answer_eviction.pdf`,
          category: 'eviction',
          partyType: 'tenant',
          fileType: 'pdf',
          filingFee: 0
        },
        {
          id: 'fl-eviction-004',
          name: 'Motion for Default',
          description: 'Request for default judgment if tenant fails to respond',
          url: `https://www.flcourts.org/content/download/404315/file/form_0040_motion_default.pdf`,
          category: 'eviction',
          partyType: 'landlord',
          fileType: 'pdf',
          filingFee: 0
        },
        {
          id: 'fl-eviction-005',
          name: 'Motion to Determine Amount of Rent',
          description: 'Used when tenant disputes amount of rent owed',
          url: `https://www.flcourts.org/content/download/404317/file/form_0042_motion_determine_rent.pdf`,
          category: 'eviction',
          partyType: 'tenant',
          fileType: 'pdf',
          filingFee: 0
        }
      ],
      'landlordTenant': [
        {
          id: 'fl-lt-001',
          name: 'Three-Day Notice to Pay Rent or Vacate',
          description: 'Preliminary notice before filing eviction for non-payment',
          url: `https://www.flcourts.org/content/download/404319/file/form_0043_3day_notice.pdf`,
          category: 'landlordTenant',
          partyType: 'landlord',
          fileType: 'pdf',
          filingFee: 0
        },
        {
          id: 'fl-lt-002',
          name: 'Security Deposit Dispute Form',
          description: 'Form to dispute a security deposit claim',
          url: `https://www.flcourts.org/content/download/404321/file/form_0045_security_deposit.pdf`,
          category: 'landlordTenant',
          partyType: 'tenant',
          fileType: 'pdf',
          filingFee: 0
        }
      ],
      'smallClaims': [
        {
          id: 'fl-sc-001',
          name: 'Small Claims Statement of Claim',
          description: 'Initial filing for small claims cases (under $8,000)',
          url: `https://www.flcourts.org/content/download/404325/file/form_0050_small_claim.pdf`,
          category: 'smallClaims',
          fileType: 'pdf',
          filingFee: 100.00
        },
        {
          id: 'fl-sc-002',
          name: 'Small Claims Summons',
          description: 'Summons to be served with small claims statement',
          url: `https://www.flcourts.org/content/download/404327/file/form_0052_small_claim_summons.pdf`,
          category: 'smallClaims',
          fileType: 'pdf',
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
    
    // Define filing requirements by case type
    const requirements = {
      'eviction': {
        requiredDocuments: [
          { name: 'Complaint for Eviction', description: 'Must be properly completed and signed' },
          { name: 'Copy of Lease Agreement', description: 'Complete copy of the lease with all pages and signatures' },
          { name: 'Notice to Tenant', description: 'Copy of the notice given to tenant (3-day, 7-day, etc.)' },
          { name: 'Civil Cover Sheet', description: 'Florida Civil Cover Sheet completed and signed' },
          { name: 'Summons', description: 'One summons for each tenant being evicted' }
        ],
        filingFee: 185.00,
        filingMethods: [
          { 
            method: 'Online',
            url: `https://www.mypinellasclerk.org/Home/E-Filing`,
            description: 'File through the Florida Courts E-Filing Portal'
          },
          { 
            method: 'In Person',
            location: `${county} County Courthouse`,
            hours: 'Monday-Friday 8:30am-5:00pm',
            description: 'File at the Civil Division clerk\'s office'
          }
        ],
        specialInstructions: [
          '1. Ensure all notices have been properly served to the tenant before filing',
          '2. Provide accurate contact information for all parties',
          '3. Include the correct filing fee or request for waiver of fee',
          '4. For non-payment evictions, a copy of the 3-day notice must be included'
        ],
        statutoryReferences: [
          'Florida Statutes Chapter 83, Part II - Florida Residential Landlord and Tenant Act',
          'Florida Statutes Section 83.59 - Right of action for possession',
          'Florida Statutes Section 83.56 - Termination of rental agreement'
        ]
      },
      'security_deposit': {
        requiredDocuments: [
          { name: 'Statement of Claim', description: 'Detailing the security deposit dispute' },
          { name: 'Copy of Lease Agreement', description: 'Complete copy of the lease with all pages and signatures' },
          { name: 'Itemized List', description: 'Itemized list of deductions or claims on the security deposit' },
          { name: 'Proof of Notice', description: 'Proof of written notice regarding the security deposit' }
        ],
        filingFee: 100.00,
        filingMethods: [
          { 
            method: 'Online',
            url: `https://www.mypinellasclerk.org/Home/E-Filing`,
            description: 'File through the Florida Courts E-Filing Portal'
          },
          { 
            method: 'In Person',
            location: `${county} County Courthouse`,
            hours: 'Monday-Friday 8:30am-5:00pm',
            description: 'File at the Civil Division clerk\'s office'
          }
        ],
        specialInstructions: [
          '1. Ensure compliance with Florida Statute 83.49 regarding security deposit handling',
          '2. Include all correspondence related to the security deposit claim',
          '3. Provide clear documentation of damages with receipts or estimates'
        ],
        statutoryReferences: [
          'Florida Statutes Section 83.49 - Deposit money or advance rent; duty of landlord',
          'Florida Statutes Section 83.50 - Disclosure of landlord\'s address'
        ]
      },
      'smallClaims': {
        requiredDocuments: [
          { name: 'Statement of Claim', description: 'Detail the claim and relief sought' },
          { name: 'Supporting Documents', description: 'Any documents supporting the claim' },
          { name: 'Civil Cover Sheet', description: 'Florida Civil Cover Sheet completed and signed' }
        ],
        filingFee: 100.00,
        filingMethods: [
          { 
            method: 'Online',
            url: `https://www.mypinellasclerk.org/Home/E-Filing`,
            description: 'File through the Florida Courts E-Filing Portal'
          },
          { 
            method: 'In Person',
            location: `${county} County Courthouse`,
            hours: 'Monday-Friday 8:30am-5:00pm',
            description: 'File at the Civil Division clerk\'s office'
          }
        ],
        specialInstructions: [
          '1. Claims must be for $8,000 or less to qualify for small claims court',
          '2. Include correct addresses for all parties',
          '3. Pre-trial mediation is generally required before a trial'
        ],
        statutoryReferences: [
          'Florida Small Claims Rules',
          'Florida Statutes Chapter 34 - County Courts'
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
    
    // Define precedent cases by issue type
    const precedents = {
      'eviction': [
        {
          id: 'fl-prec-001',
          caseName: 'Brown v. Aldrich',
          citation: '316 So.3d 719 (Fla. 2d DCA 2021)',
          summary: 'Landlord must strictly comply with statutory notice requirements before filing an eviction action',
          statutes: ['F.S. 83.56'],
          holding: 'Failure to provide proper notice is an absolute defense to an eviction action'
        },
        {
          id: 'fl-prec-002',
          caseName: 'Flannery v. Green Palm Investments, LLC',
          citation: '304 So.3d 1273 (Fla. 1st DCA 2020)',
          summary: 'Addresses deposit of rent into court registry during pendency of eviction proceedings',
          statutes: ['F.S. 83.60'],
          holding: 'Failure to deposit rent into court registry can result in default judgment'
        }
      ],
      'security_deposit': [
        {
          id: 'fl-prec-003',
          caseName: 'Merrill v. Hooper',
          citation: '269 So.3d 542 (Fla. 2d DCA 2019)',
          summary: 'Addresses landlord obligations regarding security deposit itemization',
          statutes: ['F.S. 83.49'],
          holding: 'Landlord must provide timely, itemized deduction notice or forfeit right to claim damages'
        }
      ],
      'habitability': [
        {
          id: 'fl-prec-004',
          caseName: 'Hialeah Housing Authority v. Blanco',
          citation: '115 So.3d 1025 (Fla. 3d DCA 2013)',
          summary: 'Addresses tenant rights regarding habitability issues',
          statutes: ['F.S. 83.51'],
          holding: 'Landlords must maintain premises in compliance with building, housing, and health codes'
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

module.exports = FloridaCourtConnector;