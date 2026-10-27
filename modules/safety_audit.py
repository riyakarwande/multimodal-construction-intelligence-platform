"""
Site Safety & PPE Audit Engine (Epic 2)
Analyzes construction site photos for worker PPE compliance and OSHA / IS 456 standards.
Generates structured JSON data contracts, metrics, and actionable corrective remedies.
"""

import json
from datetime import datetime
from typing import Dict, Any, List

SAFETY_SYSTEM_PROMPT = """
You are a Principal Site Safety Auditor and Chief Civil Safety Officer certified under OSHA (29 CFR 1926) and Indian Standard IS 456 / IS 3521 / IS 2925.
Analyze the provided construction site photograph with forensic precision.

You must return your evaluation strictly as a valid JSON object matching this schema:
{
  "safety_score": <integer from 0 to 100>,
  "overall_status": "<Compliant | Conditional Pass | Critical Violation>",
  "worker_count_estimate": <integer>,
  "ppe_detection": {
    "helmets": {
      "detected": <boolean>,
      "compliance_rate": "<e.g. 75%>",
      "status": "<Compliant | Partial Non-Compliance | Critical Violation>",
      "notes": "<observation string>"
    },
    "high_vis_vests": {
      "detected": <boolean>,
      "compliance_rate": "<e.g. 100%>",
      "status": "<Compliant | Partial Non-Compliance | Critical Violation>",
      "notes": "<observation string>"
    },
    "steel_toe_boots": {
      "detected": <boolean>,
      "compliance_rate": "<e.g. 50%>",
      "status": "<Compliant | Partial Non-Compliance | Critical Violation>",
      "notes": "<observation string>"
    },
    "safety_harnesses": {
      "detected": <boolean>,
      "compliance_rate": "<e.g. 0% or N/A>",
      "status": "<Compliant | Critical Hazard | Not Required at Grade>",
      "notes": "<observation string>"
    },
    "eye_face_protection": {
      "detected": <boolean>,
      "compliance_rate": "<e.g. 60%>",
      "status": "<Compliant | Advisory>",
      "notes": "<observation string>"
    }
  },
  "identified_hazards": [
    {
      "hazard": "<description of hazard>",
      "severity": "<Critical | High | Medium | Low>",
      "location": "<location within frame, e.g. Scaffolding Tier 3>",
      "standard_violated": "<e.g. OSHA 1926.502 / IS 3521>",
      "corrective_remedy": "<immediate corrective engineering action>"
    }
  ],
  "applicable_standards": [
    "OSHA 1926.100 / IS 2925 (Head Protection)",
    "OSHA 1926.201 / EN ISO 20471 (High-Visibility Apparel)",
    "OSHA 1926.502 / IS 3521 (Fall Arrest Systems)",
    "IS 456:2000 (General Construction Safety)"
  ],
  "audit_summary": "<summary paragraph of findings and immediate site manager directives>"
}

Do not include any commentary outside the JSON block.
"""

SAFETY_USER_PROMPT = """
Inspect this construction site image. Detect all visible personnel, assess their Personal Protective Equipment (helmets, high-vis vests, steel-toe boots, safety harness tie-offs, safety glasses), identify any physical site hazards (unprotected edges, scaffolding flaws, rebar impalement risks, trip hazards), and return the full structured JSON audit report.
"""


def generate_mock_safety_audit(scenario_type: str = "scaffold_hazard") -> Dict[str, Any]:
    """Generates realistic structured safety audit data for fallback demonstration mode."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    
    if scenario_type == "compliant":
        return {
            "safety_score": 96,
            "overall_status": "Compliant",
            "worker_count_estimate": 3,
            "ppe_detection": {
                "helmets": {
                    "detected": True,
                    "compliance_rate": "100%",
                    "status": "Compliant",
                    "notes": "All 3 workers wearing hard hats meeting IS 2925 / ANSI Z89.1 Class E standards."
                },
                "high_vis_vests": {
                    "detected": True,
                    "compliance_rate": "100%",
                    "status": "Compliant",
                    "notes": "Fluorescent high-vis orange/green safety vests with retroreflective tape visible."
                },
                "steel_toe_boots": {
                    "detected": True,
                    "compliance_rate": "100%",
                    "status": "Compliant",
                    "notes": "Heavy duty puncture-resistant steel toe safety boots observed per IS 15298."
                },
                "safety_harnesses": {
                    "detected": False,
                    "compliance_rate": "N/A",
                    "status": "Not Required at Grade",
                    "notes": "Work conducted in grade excavation trench with slope protection; fall arrest not triggered."
                },
                "eye_face_protection": {
                    "detected": True,
                    "compliance_rate": "100%",
                    "status": "Compliant",
                    "notes": "UV impact-resistant safety glasses donned during rebar fabrication."
                }
            },
            "identified_hazards": [
                {
                    "hazard": "Exposed starter rebar dowels in adjoining bay without mushroom safety caps",
                    "severity": "Medium",
                    "location": "Trench boundary adjacent to Zone 2",
                    "standard_violated": "OSHA 1926.701(b) / IS 456 Cl. 12",
                    "corrective_remedy": "Fit high-visibility plastic impalement safety caps over all exposed vertical rebar ends immediately."
                },
                {
                    "hazard": "Gravel aggregate spillage along perimeter pedestrian corridor",
                    "severity": "Low",
                    "location": "Walkway Zone 1",
                    "standard_violated": "OSHA 1926.25 Housekeeping",
                    "corrective_remedy": "Clear loose aggregate and maintain clear demarcated 1.2m access paths."
                }
            ],
            "applicable_standards": [
                "OSHA 1926.100 / IS 2925 (Industrial Safety Helmets)",
                "OSHA 1926.201 / EN ISO 20471 (High-Visibility Workwear)",
                "OSHA 1926.96 / IS 15298 (Protective Footwear)",
                "OSHA 1926.701 / IS 456 (Concrete & Rebar Impalement Protection)"
            ],
            "audit_summary": "Exemplary site safety adherence observed among the trench excavation rebar crew. 100% compliance recorded for hard hats, high-vis vests, and steel-toe boots. Remedial action is confined to secondary housekeeping and installing rebar mushroom caps.",
            "timestamp": now_str,
            "engine_mode": "Demonstration Synthetic Model"
        }
    else:
        # High Risk Scaffolding Hazard Scenario
        return {
            "safety_score": 42,
            "overall_status": "Critical Violation",
            "worker_count_estimate": 2,
            "ppe_detection": {
                "helmets": {
                    "detected": True,
                    "compliance_rate": "50%",
                    "status": "Critical Violation",
                    "notes": "Worker 1 on ground has hardhat. Worker 2 on elevated scaffolding lacks head protection."
                },
                "high_vis_vests": {
                    "detected": True,
                    "compliance_rate": "50%",
                    "status": "Partial Non-Compliance",
                    "notes": "Worker 2 on scaffolding wearing non-reflective street clothing, invisible in low light."
                },
                "steel_toe_boots": {
                    "detected": True,
                    "compliance_rate": "50%",
                    "status": "Partial Non-Compliance",
                    "notes": "Elevated worker appears to be wearing standard canvas/rubber sneakers without puncture plates."
                },
                "safety_harnesses": {
                    "detected": False,
                    "compliance_rate": "0%",
                    "status": "Critical Hazard",
                    "notes": "CRITICAL HAZARD: Worker working at height (>3.5m) on scaffolding level 3 without full body harness or anchorage lifeline."
                },
                "eye_face_protection": {
                    "detected": False,
                    "compliance_rate": "0%",
                    "status": "Advisory",
                    "notes": "No safety eyewear or face shield observed."
                }
            },
            "identified_hazards": [
                {
                    "hazard": "Fall Hazard at Elevated Height without Fall Arrest System",
                    "severity": "Critical",
                    "location": "Upper Scaffolding Tier (Level 3, >3.5m elevation)",
                    "standard_violated": "OSHA 1926.502 / IS 3521 / BOCW Act 1996",
                    "corrective_remedy": "Issue immediate STOP-WORK ORDER. Worker must descend safely; install certified static horizontal lifeline and enforce double-lanyard 100% tie-off harness."
                },
                {
                    "hazard": "Absence of Hard Hat in Active Overhead Construction Zone",
                    "severity": "Critical",
                    "location": "Elevated staging platform",
                    "standard_violated": "OSHA 1926.100 / IS 2925",
                    "corrective_remedy": "Provide EN 397 / IS 2925 Class E industrial helmet with chinstrap before permitting access."
                },
                {
                    "hazard": "Missing Guardrails and Toeboards on Working Platform",
                    "severity": "High",
                    "location": "Scaffolding Level 3 bay",
                    "standard_violated": "OSHA 1926.451(g)(1) / IS 4014",
                    "corrective_remedy": "Install top guardrail (42 inches), mid-rail (21 inches), and 4-inch kick toeboard along open scaffold perimeter."
                },
                {
                    "hazard": "Lack of High-Visibility Safety Apparel",
                    "severity": "Medium",
                    "location": "Scaffold working platform",
                    "standard_violated": "OSHA 1926.201 / EN ISO 20471",
                    "corrective_remedy": "Equip worker with Class 2 high-visibility reflective waistcoat."
                }
            ],
            "applicable_standards": [
                "OSHA 1926.502 / IS 3521 (Fall Protection & Harness Mandates)",
                "OSHA 1926.100 / IS 2925 (Occupational Head Protection)",
                "OSHA 1926.451 / IS 4014 (Scaffolding Safety & Guardrails)",
                "OSHA 1926.201 (High-Visibility Safety Apparel)"
            ],
            "audit_summary": "IMMEDIATE INTERVENTION REQUIRED. Life-critical fall hazards detected on elevated scaffolding. An operative is exposed to fatal fall risk without safety harness or perimeter guardrails. Stop-work directive issued for scaffold bay until full OSHA 1926.502 compliance is certified by the site safety supervisor.",
            "timestamp": now_str,
            "engine_mode": "Demonstration Synthetic Model"
        }


def format_ppe_checklist_markdown(ppe_data: Dict[str, Any]) -> str:
    """Formats PPE compliance results into clean markdown table."""
    md = "| PPE Item | Detected | Compliance Rate | Status | Findings |\n"
    md += "| :--- | :---: | :---: | :---: | :--- |\n"
    
    labels = {
        "helmets": "🪖 Safety Helmets (IS 2925)",
        "high_vis_vests": "🦺 High-Vis Vests (EN 20471)",
        "steel_toe_boots": "🥾 Steel-Toe Boots (IS 15298)",
        "safety_harnesses": "🧗 Fall Arrest Harness (IS 3521)",
        "eye_face_protection": "🥽 Eye / Face Protection (OSHA)"
    }
    
    for key, label in labels.items():
        item = ppe_data.get(key, {})
        detected = "✅ Yes" if item.get("detected") else "❌ No"
        rate = item.get("compliance_rate", "N/A")
        status = item.get("status", "Unknown")
        notes = item.get("notes", "—")
        md += f"| {label} | {detected} | {rate} | **{status}** | {notes} |\n"
        
    return md
