import json

nomic_data = []

# Financial Contribution Visualization
# Property Expenses Since October 2023
financial_expenses = [
    {"period": "Oct-Dec 2023", "total_expenses": "$10,500", "stephen_contribution": "$7,500", "melissa_contribution": "$3,000", "stephen_percent": "71.4%", "melissa_percent": "28.6%"},
    {"period": "Jan-Jun 2024", "total_expenses": "$21,000", "stephen_contribution": "$17,000", "melissa_contribution": "$4,000", "stephen_percent": "81.0%", "melissa_percent": "19.0%"},
    {"period": "Jul-Sep 2024", "total_expenses": "$10,500", "stephen_contribution": "$10,000", "melissa_contribution": "$500", "stephen_percent": "95.2%", "melissa_percent": "4.8%"},
    {"period": "Oct-Dec 2024", "total_expenses": "$10,500", "stephen_contribution": "$10,500", "melissa_contribution": "$0", "stephen_percent": "100%", "melissa_percent": "0%"},
    {"period": "Jan-Mar 2025", "total_expenses": "$10,500", "stephen_contribution": "$10,500", "melissa_contribution": "$0", "stephen_percent": "100%", "melissa_percent": "0%"},
]

for item in financial_expenses:
    nomic_data.append({
        "text": f"Property expenses for {item['period']}: Stephen contributed {item['stephen_contribution']} ({item['stephen_percent']}), Melissa contributed {item['melissa_contribution']} ({item['melissa_percent']}). Total expenses: {item['total_expenses']}.",
        "category": "Financial Contribution",
        "date_period": item['period'],
        "source_document": "evidence matrix.txt",
        "legal_theory_supported": "Financial Abandonment, Preservation Credit",
        "contribution_type": "Regular Expenses"
    })

# Additional Preservation Investments
additional_investments = [
    {"investment": "HVAC Replacement", "date": "Jul 2023", "amount": "$12,000", "stephen_percent": "100%", "melissa_percent": "0%"},
    {"investment": "Bridge Loan", "date": "Jan 3, 2025", "amount": "$12,500", "stephen_percent": "100%", "melissa_percent": "0%"},
]

for item in additional_investments:
    nomic_data.append({
        "text": f"Additional investment: {item['investment']} on {item['date']} for {item['amount']}. Stephen contributed {item['stephen_percent']}, Melissa contributed {item['melissa_percent']}.",
        "category": "Financial Contribution",
        "date": item['date'],
        "source_document": "evidence matrix.txt",
        "legal_theory_supported": "Preservation Credit",
        "contribution_type": "Additional Investment"
    })

# Total Preservation Contribution
nomic_data.append({
    "text": "Total preservation contribution: Stephen $80,000 (91.4%), Melissa $7,500 (8.6%). Total $87,500.",
    "category": "Financial Contribution",
    "source_document": "evidence matrix.txt",
    "legal_theory_supported": "Preservation Credit, Financial Abandonment",
    "contribution_type": "Total"
})

# Timeline Visualization Evidence - TRAUMA PIVOT POINT (March 26, 2024)
timeline_events = [
    {"type": "Pre-Trauma", "event": "Joint property acquisition", "date": "Apr 15, 2022", "source": "evidence matrix.txt", "legal_theory": "N/A"},
    {"type": "Pre-Trauma", "event": "HVAC investment", "date": "Jul 2023", "source": "evidence matrix.txt", "legal_theory": "Preservation Credit"},
    {"type": "Pre-Trauma", "event": "Rental management", "date": "Oct 2023-Sep 2024", "source": "evidence matrix.txt", "legal_theory": "N/A"},
    {"type": "Pre-Trauma", "event": "\"Very good\" marriage documentation", "date": "N/A", "source": "evidence matrix.txt", "legal_theory": "N/A"},
    {"type": "Pre-Trauma", "event": "Joint business ventures", "date": "Jan-Mar 2024", "source": "evidence matrix.txt", "legal_theory": "N/A"},
    {"type": "Pivot Point", "event": "Home invasion documentation", "date": "Mar 26, 2024", "source": "evidence matrix.txt", "legal_theory": "Disability Impact"},
    {"type": "Pivot Point", "event": "Police report", "date": "Mar 26, 2024", "source": "evidence matrix.txt", "legal_theory": "Disability Impact"},
    {"type": "Pivot Point", "event": "Medical records (related to trauma)", "date": "N/A", "source": "evidence matrix.txt", "legal_theory": "Disability Impact"},
    {"type": "Pivot Point", "event": "Witness statements (related to trauma)", "date": "N/A", "source": "evidence matrix.txt", "legal_theory": "Disability Impact"},
    {"type": "Post-Trauma", "event": "PTSD/ADHD diagnosis", "date": "Mar/Apr 2024", "source": "evidence matrix.txt", "legal_theory": "Disability Impact"},
    {"type": "Post-Trauma", "event": "Medical treatment timeline", "date": "N/A", "source": "evidence matrix.txt", "legal_theory": "Disability Impact"},
    {"type": "Post-Trauma", "event": "Insurance through Wife's employment", "date": "May 2024", "source": "evidence matrix.txt", "legal_theory": "N/A"},
    {"type": "Post-Trauma", "event": "Wife's attendance at medical appointments", "date": "Jun 2024", "source": "evidence matrix.txt", "legal_theory": "N/A"},
    {"type": "Post-Trauma", "event": "FMLA rejection documentation", "date": "Jul 2024", "source": "evidence matrix.txt", "legal_theory": "Financial Abandonment"},
    {"type": "Post-Trauma", "event": "Wife's employment termination", "date": "Jul 28-29, 2024", "source": "evidence matrix.txt", "legal_theory": "Financial Abandonment"},
    {"type": "Post-Trauma", "event": "Wife's return to PA leaving Husband in FL", "date": "N/A", "source": "evidence matrix.txt", "legal_theory": "Financial Abandonment"},
    {"type": "Post-Trauma", "event": "Health insurance termination", "date": "Aug 2024", "source": "evidence matrix.txt", "legal_theory": "Financial Abandonment"},
    {"type": "Post-Trauma", "event": "Zero contribution period", "date": "Oct 2024-Present", "source": "evidence matrix.txt", "legal_theory": "Financial Abandonment"},
]

for item in timeline_events:
    nomic_data.append({
        "text": f"{item['type']} event: {item['event']}. Date: {item['date']}.",
        "category": "Timeline Event",
        "event_type": item['type'],
        "date": item['date'],
        "source_document": item['source'],
        "legal_theory_supported": item['legal_theory']
    })

# Critical Deadlines
critical_deadlines = [
    {"event": "Bridge Loan Exhaustion", "date": "March 16, 2025", "priority": "CRITICAL", "action": "Document final covered payment"},
    {"event": "First Day of Unpaid Period", "date": "March 17, 2025", "priority": "HIGH", "action": "Document beginning of crisis period"},
    {"event": "Emergency Motion Filing", "date": "By April 15, 2025", "priority": "CRITICAL", "action": "Complete motion and documentation"},
    {"event": "First Missed Payment", "date": "April 16, 2025", "priority": "CRITICAL", "action": "Document default trigger"},
    {"event": "Act 91 Notice Expected", "date": "Within 30 days of default", "priority": "HIGH", "action": "Prepare response strategy"},
    {"event": "Right to Cure Period Ends", "date": "Approx. May 16, 2025", "priority": "HIGH", "action": "Ensure court intervention before this date"},
    {"event": "Potential Sheriff's Sale", "date": "July-August 2025", "priority": "HIGH", "action": "Must prevent through court action"},
]

for item in critical_deadlines:
    nomic_data.append({
        "text": f"Critical Deadline: {item['event']} by {item['date']}. Priority: {item['priority']}. Action: {item['action']}.",
        "category": "Critical Deadline",
        "date": item['date'],
        "priority": item['priority'],
        "action_required": item['action'],
        "source_document": "evidence matrix.txt"
    })

# Legal Theories (summarized from the matrix)
legal_theories = [
    {"name": "Financial Abandonment Doctrine", "statute": "23 Pa.C.S. § 3502(a)(7), (10)", "description": "Establishes contribution disparity, insurance termination, FMLA rejection, zero contribution period, and current income disparity."},
    {"name": "Preservation Credit Principle", "statute": "23 Pa.C.S. § 3502(a)(7)", "description": "Covers HVAC investment, bridge loan, monthly expenses, realtor communications, and property value preservation."},
    {"name": "Disability Impact Factor", "statute": "23 Pa.C.S. § 3502(a)(3)", "description": "Relates to medical diagnosis, treatment timeline, insurance impact, employment impact, and traumatic event."},
    {"name": "Foreclosure Risk Documentation", "statute": "23 Pa.C.S. § 3323(f), 3502(a)(14)", "description": "Includes payment history, bridge loan exhaustion, equity at risk, foreclosure timeline, and settlement attempts."},
]

for item in legal_theories:
    nomic_data.append({
        "text": f"Legal Theory: {item['name']}. Statutory Reference: {item['statute']}. Description: {item['description']}",
        "category": "Legal Theory",
        "name": item['name'],
        "statute": item['statute'],
        "source_document": "evidence matrix.txt"
    })

# Output the data to a JSON file for review
with open("nomic_atlas_data.json", "w") as f:
    json.dump(nomic_data, f, indent=4)

print(f"Generated {len(nomic_data)} data points for Nomic Atlas in nomic_atlas_data.json")