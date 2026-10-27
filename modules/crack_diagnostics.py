"""
Crack Diagnostics & Structural Integrity Engine (Epic 2)
Forensic multimodal classification of concrete defects under IS 456:2000 and ACI 224R.
Classifies crack types, estimates crack width in mm, determines severity scores, root causes, and recommended engineering repairs.
"""

from datetime import datetime
from typing import Dict, Any, List

CRACK_SYSTEM_PROMPT = """
You are a Senior Forensic Structural Engineer and Concrete Technology Specialist specializing in IS 456:2000, ACI 224R (Control of Cracking in Concrete Structures), and ASTM C881.
Analyze the provided concrete or masonry surface photograph.

Classify the defect into one of the following primary categories:
1. "Hairline Crack" (Plastic shrinkage / Crazing)
2. "Settlement Crack" (Differential foundation movement)
3. "Structural Shear Crack" (Shear / Flexural overload)
4. "Thermal Expansion Crack" (Seasonal cyclic thermal strain)
5. "Spalling / Concrete Delamination" (Rebar corrosion & cover loss)

Return strictly a valid JSON object matching this schema:
{
  "defect_type": "<Hairline Crack | Settlement Crack | Structural Shear Crack | Thermal Expansion Crack | Spalling / Delamination>",
  "estimated_crack_width_mm": <float, e.g. 2.85>,
  "severity_score": <integer from 0 to 100>,
  "structural_risk_level": "<Low | Moderate | High | Critical>",
  "urgency": "<Immediate (24-48h) | Priority (7-14 Days) | Routine Maintenance (30+ Days)>",
  "is_456_compliance": {
    "permissible_limit_mm": "<0.30mm (Mild) | 0.20mm (Moderate) | 0.10mm (Severe)>",
    "exceeds_limit": <boolean>,
    "compliance_verdict": "<Compliant | Marginal Non-Compliance | Severe Code Violation>"
  },
  "root_causes": [
    "<primary structural or chemical cause>",
    "<secondary environmental or loading cause>"
  ],
  "affected_elements": [
    "<e.g. RCC Beam B-104 shear zone, Slab soffit, Masonry wall>"
  ],
  "recommended_engineering_repairs": [
    {
      "step": 1,
      "method": "<e.g. Low-Pressure Epoxy Resin Injection / CFRP Jacketing>",
      "specification": "<e.g. ASTM C881 Type I / IV structural resin>",
      "procedure": "<step-by-step application instructions>"
    }
  ],
  "monitoring_protocol": "<recommended ongoing instrumentation, e.g. Avongard tell-tale crack width gauge>",
  "engineering_summary": "<concise paragraph summarizing diagnosis and immediate structural recommendations>"
}

Do not include any text outside the JSON block.
"""

CRACK_USER_PROMPT = """
Inspect this structural surface image. Measure or estimate the crack width in millimeters, classify the defect type (Hairline, Settlement, Structural Shear, Thermal Expansion, or Spalling), identify root causes, determine IS 456 compliance, and formulate step-by-step structural repair specifications.
"""


def generate_mock_crack_diagnostics(defect_hint: str = "shear") -> Dict[str, Any]:
    """Generates realistic structural diagnostics data for fallback demonstration mode."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    
    if "hairline" in defect_hint.lower():
        return {
            "defect_type": "Hairline Crack",
            "estimated_crack_width_mm": 0.12,
            "severity_score": 18,
            "structural_risk_level": "Low",
            "urgency": "Routine Maintenance (30+ Days)",
            "is_456_compliance": {
                "permissible_limit_mm": "0.30mm (Mild Exposure)",
                "exceeds_limit": False,
                "compliance_verdict": "Compliant (Within IS 456 Cl. 35.3.2 Limits)"
            },
            "root_causes": [
                "Plastic shrinkage during early stage hydration due to rapid surface water evaporation",
                "High ambient wind and low relative humidity during initial 48-hour curing window",
                "Superficial plaster mortar rich mix ratio (1:3) causing shrinkage crazing"
            ],
            "affected_elements": [
                "Non-structural internal plaster finish and superficial concrete cover"
            ],
            "recommended_engineering_repairs": [
                {
                    "step": 1,
                    "method": "V-Groove Routing & Surface Cleaning",
                    "specification": "ASTM C1059 / Surface prep",
                    "procedure": "Rake open crack surface to 2mm x 2mm V-groove using mechanical crack chaser; blow clean with oil-free compressed air."
                },
                {
                    "step": 2,
                    "method": "Elastomeric Micro-Polymer Surface Sealer",
                    "specification": "Single-component acrylic elastomeric crack filler",
                    "procedure": "Apply flexible elastomeric polymer sealant flush with surface, allow 24h cure, and apply anti-carbonation protective paint."
                }
            ],
            "monitoring_protocol": "Visual inspection during quarterly maintenance audit; crack does not affect primary load-bearing capacity.",
            "engineering_summary": "Superficial hairline crazing confirmed with estimated aperture of 0.12mm. The defect is non-structural, fully compliant with IS 456:2000 (0.30mm permissible threshold), and requires only cosmetic elastomeric surface sealing.",
            "timestamp": now_str,
            "engine_mode": "Demonstration Synthetic Model"
        }
    elif "spall" in defect_hint.lower():
        return {
            "defect_type": "Spalling / Concrete Delamination",
            "estimated_crack_width_mm": 45.0,
            "severity_score": 88,
            "structural_risk_level": "Critical",
            "urgency": "Immediate (24-48h)",
            "is_456_compliance": {
                "permissible_limit_mm": "0.10mm (Severe Marine) / Spall Violation",
                "exceeds_limit": True,
                "compliance_verdict": "Severe Code Violation (Exposed Corroded Rebar)"
            },
            "root_causes": [
                "Advanced carbonation and chloride penetration depassivating the steel alkaline protective layer",
                "Volumetric expansion (2.5x to 4x) of ferric oxide corrosion products causing radial bursting tensile stresses",
                "Inadequate clear concrete cover (<25mm instead of required 40mm nominal cover per IS 456 Cl. 26.4)"
            ],
            "affected_elements": [
                "Column C-12 primary vertical reinforcement and concrete outer cover"
            ],
            "recommended_engineering_repairs": [
                {
                    "step": 1,
                    "method": "Hydro-Demolition & Sound Concrete Boundary Definition",
                    "specification": "ICRI Technical Guideline No. 310.1R",
                    "procedure": "Chisel back loose concrete 20mm behind exposed corroded rebar until sound, uncarbonated concrete substrate is reached."
                },
                {
                    "step": 2,
                    "method": "Rebar De-Rusting & Zinc-Rich Anti-Corrosion Primer",
                    "specification": "ASTM A775 / Zinc-rich 2-part epoxy primer",
                    "procedure": "Grit-blast or mechanically wire-brush rebar to bare metal (Sa 2.5); apply 2 coats of zinc-rich anti-corrosion primer within 4 hours."
                },
                {
                    "step": 3,
                    "method": "Polymer Modified Mortar (PMM) Build-up & Structural Jacketing",
                    "specification": "EN 1504-3 Class R4 structural mortar",
                    "procedure": "Apply bonding agent; build up structural repair mortar in 20mm passes; cure under damp burlap for 7 days."
                }
            ],
            "monitoring_protocol": "Half-cell potential testing (ASTM C876) across adjacent column zones to identify latent active galvanic corrosion sites.",
            "engineering_summary": "Severe spalling defect with 45mm cover detachment and direct atmospheric exposure of corroded primary rebar. Significant loss of rebar cross-sectional area detected (~20%). Urgent structural rehabilitation required to prevent progressive column buckling under dead load.",
            "timestamp": now_str,
            "engine_mode": "Demonstration Synthetic Model"
        }
    else:
        # Default: Structural Shear Crack
        return {
            "defect_type": "Structural Shear Crack",
            "estimated_crack_width_mm": 2.85,
            "severity_score": 92,
            "structural_risk_level": "Critical",
            "urgency": "Immediate (24-48h)",
            "is_456_compliance": {
                "permissible_limit_mm": "0.30mm (IS 456 Cl. 35.3.2 Max)",
                "exceeds_limit": True,
                "compliance_verdict": "Critical Structural Violation (9.5x Permissible Limit)"
            },
            "root_causes": [
                "Principal diagonal tensile stress exceeding concrete shear strength (tau_c) under heavy shear loading",
                "Deficient shear stirrup reinforcement spacing or redistribution of moment due to column differential settlement",
                "Cyclic thermal deflection exacerbating active crack propagation along 45-degree shear trajectory"
            ],
            "affected_elements": [
                "RCC Beam B-104 critical shear span (within 2d from column face)"
            ],
            "recommended_engineering_repairs": [
                {
                    "step": 1,
                    "method": "Temporary Telescopic Acrow Prop Shoring",
                    "specification": "IS 4014 (Code of practice for steel tubular scaffolding)",
                    "procedure": "Immediately relieve shear stress by installing 4 heavy-duty telescopic steel props directly beneath beam B-104."
                },
                {
                    "step": 2,
                    "method": "High-Pressure Structural Epoxy Resin Injection",
                    "specification": "ASTM C881 Type I, Grade 1, Class B/C Low-Viscosity Epoxy",
                    "procedure": "Drill injection ports at 150mm intervals along crack line; seal surface with rapid-setting thixotropic epoxy paste; inject epoxy from lowest port upwards at 3-5 bar until resin oozes from adjacent port."
                },
                {
                    "step": 3,
                    "method": "Carbon Fiber Reinforced Polymer (CFRP) Shear Laminate Wrapping",
                    "specification": "ACI 440.2R-17 (CFRP composite design)",
                    "procedure": "Apply bidirectional carbon fiber fabric U-wraps anchored with mechanical composite anchors to restore and enhance ultimate shear capacity by >40%."
                }
            ],
            "monitoring_protocol": "Install calibrated Avongard two-dimensional tell-tale optical crack displacement gauges to track continuing dynamic movement.",
            "engineering_summary": "CRITICAL STRUCTURAL DEFECT. Active 45° diagonal shear crack measuring 2.85 mm detected near beam support. This is 9.5 times the permissible threshold specified in IS 456:2000 Cl. 35.3.2. Temporary shoring must be erected immediately, followed by high-pressure epoxy injection and external CFRP composite wrapping.",
            "timestamp": now_str,
            "engine_mode": "Demonstration Synthetic Model"
        }
