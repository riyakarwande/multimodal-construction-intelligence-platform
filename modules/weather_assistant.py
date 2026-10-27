"""
Weather-Aware Site Advisory & Construction Engineering Chatbot Engine (Epic 5)
Provides dynamic weather protocols for crane operations, concrete curing, electrical safety,
and powers the multi-turn site engineering assistant.
"""

from typing import Dict, Any, List

WEATHER_PROTOCOLS = {
    "High Wind (>45 km/h / Gale)": {
        "status_color": "crimson",
        "badge": "CRITICAL GALE ADVISORY",
        "crane_status": "SUSPEND ALL TOWER CRANE & HOIST OPERATIONS",
        "crane_detail": "Lock crane slew brakes or place in designated free-weathervaning mode per manufacturer specifications. Wind speed exceeds permissible 38 km/h (20 knots) threshold.",
        "height_status": "PROHIBIT WORKING AT HEIGHTS",
        "height_detail": "Evacuate external suspended platforms, mast climbers, and scaffolding levels above 6 meters. Secure all loose ply sheets, CGI roof sheeting, and rebar bundles.",
        "concrete_protocol": "ACCELERATED EVAPORATIVE LOSS WARNING",
        "concrete_detail": "High wind accelerates plastic shrinkage cracking exponentially. Apply aluminized curing compound immediately upon bleed water disappearance or wrap with damp hessian sheets.",
        "electrical_safety": "Secure high-mast lighting towers; inspect temporary pole anchors for wind-induced swaying; check overhead line clearances.",
        "worker_welfare": "Secure eye-protection to prevent high-velocity dust & grit corneal injury; suspend perimeter window glazing operations."
    },
    "Heavy Rain / Monsoon Inundation": {
        "status_color": "blue",
        "badge": "MONSOON HAZARD PROTOCOL",
        "crane_status": "RESTRICTED / MONITOR GROUND BEARING CAPACITY",
        "crane_detail": "Inspect crane outrigger foundation mats and crawler tracks for soil softening or subsidence before any pick operation.",
        "height_status": "SLIP & FALL HAZARD - RESTRICTED",
        "height_detail": "Scaffold planks become slippery. Suspend exterior painting, waterproofing, and structural steel erection. Clear mud from access ladders.",
        "concrete_protocol": "PROHIBIT UNPROTECTED CONCRETE CASTING",
        "concrete_detail": "Do not pour open slabs during downpours as rain alters the water-cement ratio and washes away surface cement paste. If rain begins mid-pour, deploy waterproof tarpaulins and prepare emergency construction joints per IS 456 Cl. 13.4.",
        "electrical_safety": "ISOLATE TEMPORARY DISTRIBUTION BOARDS. Disconnect ground-level submersible dewatering pumps and test ELCB / RCCB trip sensitivity (30mA). Ground standing water must be pumped prior to energization.",
        "worker_welfare": "Issue high-grip waterproof gumboots, raincoats with reflective strips, and mandate designated dry rest shelters."
    },
    "Extreme Heat (>40°C / Heatwave)": {
        "status_color": "darkorange",
        "badge": "HEAT STRESS & HOT WEATHER CONCRETING",
        "crane_status": "OPERATIONAL WITH CABIN CLIMATE CONTROL",
        "crane_detail": "Ensure tower crane cabin air conditioning is operational; inspect hydraulic oil temperatures for overheating.",
        "height_status": "STAGGERED SHIFT PROTOCOL",
        "height_detail": "Limit continuous roof and rebar tying work between 12:00 PM and 3:30 PM. Provide shaded rest stations with cool potable electrolyte water.",
        "concrete_protocol": "HOT WEATHER CONCRETING PROTOCOL (IS 7861 / ACI 305R)",
        "concrete_detail": "Batch concrete with chilled mixing water or flaked ice. Place concrete at temperatures below 32°C. Extend wet curing to a minimum of 14 days under continuous moist burlap. Apply retarding plasticizers to prevent slump loss.",
        "electrical_safety": "Monitor transformer and diesel generator loads; avoid running cables across scorching metal decks without thermal insulation.",
        "worker_welfare": "Mandate mandatory 15-minute hydration breaks every hour. Train supervisors on recognizing heat exhaustion and heat stroke symptoms (OSHA WBGT Index)."
    },
    "Low Visibility / Thick Fog / Smog (<200m)": {
        "status_color": "purple",
        "badge": "LOW VISIBILITY SAFETY PROTOCOL",
        "crane_status": "MANDATORY QUALIFIED RIGGER / RADIO PROTOCOL",
        "crane_detail": "Blind lifts are strictly prohibited. The crane operator must have continuous two-way two-way walkie-talkie communication with a certified banksman/signaler. Utilize high-intensity boom tip strobe lights.",
        "height_status": "RESTRICTED TRAFFIC PERIMETER",
        "height_detail": "Ensure all edge fall barriers and floor openings are marked with high-visibility reflective tape and warning beacons.",
        "concrete_protocol": "STANDARD CONCRETING PERMITTED",
        "concrete_detail": "Ensure adequate temporary floodlighting across the casting bay and finishing zone to inspect compaction and screeding.",
        "electrical_safety": "Activate perimeter floodlights and transit route bollard lights across all site vehicular roads.",
        "worker_welfare": "Require Class 3 high-visibility jackets with reflective armbands for all pedestrians on active internal transit corridors."
    },
    "Normal / Favorable (20°C - 32°C)": {
        "status_color": "green",
        "badge": "OPTIMAL WORKING CONDITIONS",
        "crane_status": "FULL CAPACITY PERMITTED",
        "crane_detail": "Execute standard daily pre-operation checklist (limit switches, wire rope inspection, anti-collision sensor verification).",
        "height_status": "NORMAL OPERATIONS UNDER 100% TIE-OFF",
        "height_detail": "Standard fall protection rules apply: safety harnesses anchored to certified lifelines for any work above 1.8 meters.",
        "concrete_protocol": "STANDARD IS 456:2000 CURING SCHEDULE",
        "concrete_detail": "Moist curing for 7 days minimum for OPC (Ordinary Portland Cement) and 10 days for blended cements (PPC/Slag cement) as mandated by IS 456 Cl. 13.5. Maintain daily ponding on flat slabs.",
        "electrical_safety": "Routine weekly RCD test and tag inspection on power tools and extension cords.",
        "worker_welfare": "Maintain standard toolbox talk daily at 08:00 AM; replenish first aid stations and drinking water coolers."
    }
}

SITE_ENGINEER_CHAT_SYSTEM_PROMPT = """
You are the "Chief Site Civil Engineer & OSHA / IS 456 Safety Director" of a tier-1 construction project.
You possess deep technical mastery of:
- IS 456:2000 (Plain and Reinforced Concrete - Code of Practice)
- IS 1893 (Criteria for Earthquake Resistant Design of Structures)
- IS 875 Parts 1-5 (Design Loads for Buildings and Structures)
- OSHA 29 CFR 1926 (Safety and Health Regulations for Construction)
- CPWD (Central Public Works Department) Specifications
- Concrete technology: slump, water-cement ratio, striking of formwork (IS 456 Table 11), curing durations, admixtures
- Structural crack diagnostics (shear, flexure, shrinkage, settlement, spalling) and remediation (epoxy injection, micro-piling, CFRP)
- Project scheduling, CapEx tracking, and real estate valuation benchmarks in India.

Tone: Professional, authoritative, highly technical yet actionable, practical for site supervisors and project managers.
Always cite relevant Indian Standard (IS) or OSHA clauses where appropriate. Use bullet points and clear formatting.
"""

# Pre-computed rich responses for fallback demonstration mode
FALLBACK_CHAT_RESPONSES = {
    "curing": """### Concrete Curing Protocol per IS 456:2000 Cl. 13.5

Under Indian Standard **IS 456:2000 (Clause 13.5)**, the minimum curing periods are strictly governed by cement type and ambient weather conditions:

1. **Standard Ordinary Portland Cement (OPC 43 / 53 Grade):**
   - **Normal Weather:** Minimum **7 days** of continuous moist curing.
   - **Hot Weather (>40°C) or Dry / Windy conditions:** Extended to **10 days**.

2. **Blended Cements (PPC - Fly Ash / PSC - Slag Cement / Mineral Admixtures):**
   - **Normal Weather:** Minimum **10 days** due to slower pozzolanic secondary hydration.
   - **Hot Weather / Low Humidity:** Extended to **14 days**.

#### Recommended Site Curing Techniques:
- **Horizontal Slabs:** Ponding method with 50mm clay/mortar bunds kept filled with potable water.
- **Vertical Columns & Shear Walls:** Continuous wrapping with wet hessian (jute) cloth, rewetted 3-4 times daily, or spray application of ASTM C309 membrane-forming curing compound.
- **Mass Concrete (Rafts):** Monitor core-to-surface thermal differential; keep $\\Delta T < 20^\\circ\\text{C}$ to prevent thermal shock cracking.""",

    "scaffolding": """### OSHA 1926.451 & IS 4014 Scaffolding Safety Checklist

Before issuing a daily **Scaffold Safe-to-Use Green Tag**, the Site Safety Officer must audit the following points:

1. **Foundation & Base Plates:**
   - Sole boards (minimum 225mm x 38mm hardwood) placed under every screw jack base plate.
   - No scaffolding erected on soft uncompacted soil, frozen ground, or broken rubble.

2. **Structural Plumb & Bracing:**
   - Standards plumb within 1:300 vertical tolerance.
   - Diagonal ledger and transverse bracing secured at every alternate bay.
   - Scaffolding tied back into the permanent concrete structure at intervals not exceeding 4m vertically and 6m horizontally.

3. **Working Platforms:**
   - Fully decked with no gaps exceeding 25mm (1 inch).
   - Planks overlapped by at least 300mm or securely cleated.

4. **Edge Protection (Mandatory above 1.8m):**
   - Top Guardrail: Installed at $1050\\text{mm} \\pm 50\\text{mm}$ (42 inches).
   - Mid-rail: Installed at approximately $530\\text{mm}$ (21 inches).
   - Toeboard: Minimum $150\\text{mm}$ (6 inches) height to prevent falling debris.

5. **Safe Access:**
   - Internal ladder access bays with trapdoors; climbing outer scaffold tubes is strictly prohibited.""",

    "crack_width": """### Permissible Crack Width Limits under IS 456:2000 & IS 3370

Under **IS 456:2000 Cl. 35.3.2 (Serviceability Limit State of Cracking)**, surface crack widths calculated or measured on reinforced concrete must not exceed the following thresholds:

| Exposure Class | Environmental Severity | Permissible Crack Width | Typical Site Applications |
| :--- | :--- | :---: | :--- |
| **Mild** | Completely sheltered / dry interior | **0.30 mm** | Internal residential slabs, beams, columns |
| **Moderate** | Exposed to ordinary rain, humid air | **0.20 mm** | Exterior building facades, foundations |
| **Severe** | Coastal marine atmosphere, aggressive soils | **0.10 mm** | Near-shore structures, industrial fumes |
| **Very Severe / Extreme** | Direct sea water spray / tidal splash zone | **0.10 mm** + Special Cover | Marine berths, jetties, chemical processing |

#### Water Retaining Structures (IS 3370 Part 2):
- Water-retaining faces of sewage treatment plants or underground water tanks: **0.10 mm max** to avoid leakage and galvanic corrosion of rebar.

*If an existing structural crack exceeds these values, load-test or structural repair (Epoxy Injection ASTM C881 / CFRP) is mandatory.*""",

    "steel_calc": """### Structural Steel Consumption Thumb Rules (IS 456 / SP 23)

In Indian civil engineering practice, structural steel reinforcement consumption is estimated using empirical thumb rules per unit built-up area:

#### 1. Per Square Foot Thumb Rules:
- **Residential RCC Building (G+4 to G+12):** $3.5 \\text{ to } 4.5\\text{ kg/sq.ft}$
- **High-Rise Residential (G+20+ with Shear Walls):** $4.5 \\text{ to } 5.5\\text{ kg/sq.ft}$
- **Commercial Office Tower / IT Park:** $5.0 \\text{ to } 6.2\\text{ kg/sq.ft}$
- **Industrial PEB / Heavy Factory:** $6.5 \\text{ to } 8.0\\text{ kg/sq.ft}$

#### 2. Percentage of Concrete Volume ($V_c$):
- **Slabs:** $0.7\\% \\text{ to } 1.0\\% \\text{ of } V_c$ (approx. $70-80\\text{ kg/m}^3$)
- **Beams:** $1.0\\% \\text{ to } 2.0\\% \\text{ of } V_c$ (approx. $100-160\\text{ kg/m}^3$)
- **Columns:** $1.5\\% \\text{ to } 3.5\\% \\text{ of } V_c$ (up to $4\\%$ max per IS 456 Cl. 26.5.3.1)
- **Footings / Rafts:** $0.5\\% \\text{ to } 0.8\\% \\text{ of } V_c$ (approx. $50-70\\text{ kg/m}^3$)

*Example: For a 50,000 sq.ft residential high-rise @ 4.8 kg/sq.ft, total TMT Fe 500D steel requirement = $240\\text{ Metric Tonnes}$.*""",

    "excavation": """### Deep Trench Excavation Safety Protocol (>1.5m) per OSHA 1926 Subpart P & IS 3764

Excavations deeper than $1.5\\text{ meters}$ ($5\\text{ feet}$) present fatal cave-in risks and mandate strict protective engineering:

1. **Soil Classification & Slope Battering:**
   - **Type A Soil (Cohesive clay):** Safe slope ratio 3/4:1 ($53^\\circ$).
   - **Type B Soil (Silt/gravel/fissured):** Safe slope ratio 1:1 ($45^\\circ$).
   - **Type C Soil (Loose sand/submerged soil):** Safe slope ratio 1.5:1 ($34^\\circ$).

2. **Shoring & Trench Shields:**
   - Hydraulic aluminum shoring or steel trench boxes must extend at least $450\\text{mm}$ (18 inches) above the vertical soil lip.

3. **Spoil Heap Clearance:**
   - Excavated spoil piles, backhoes, and dumpers must be kept at least **$1.0\\text{ to } 1.5\\text{ meters}$ ($3\\text{ feet}$) back** from trench edges to prevent surcharge collapse.

4. **Access & Egress (OSHA 1926.651(c)):**
   - In trenches deeper than $1.2\\text{m}$ (4 feet), access ladders must be positioned within **$7.5\\text{ meters}$ (25 feet) of lateral travel distance** from any worker.
   - Ladders must project $1.0\\text{m}$ (3 rungs) above the excavation top."""
}


def get_fallback_engineering_response(user_query: str) -> str:
    """Matches user query against known civil engineering knowledge base."""
    q = user_query.lower()
    if "curing" in q or "m25" in q or "water" in q or "summer" in q:
        return FALLBACK_CHAT_RESPONSES["curing"]
    elif "scaffold" in q or "osha 1926" in q or "ladder" in q:
        return FALLBACK_CHAT_RESPONSES["scaffolding"]
    elif "crack" in q or "width" in q or "permissible" in q or "3370" in q:
        return FALLBACK_CHAT_RESPONSES["crack_width"]
    elif "steel" in q or "tmt" in q or "consumption" in q or "kg" in q or "rebar" in q:
        return FALLBACK_CHAT_RESPONSES["steel_calc"]
    elif "excavat" in q or "trench" in q or "shoring" in q or "pit" in q:
        return FALLBACK_CHAT_RESPONSES["excavation"]
    else:
        return (
            f"### Chief Site Engineer Directive\n\n"
            f"**Regarding your inquiry:** *\"{user_query}\"*\n\n"
            f"Under Indian Standards (**IS 456:2000 / IS 1893**) and **OSHA 1926 Construction Guidelines**, "
            f"ensure that all structural operations comply with certified structural drawings and site safety permits. "
            f"\n\nKey Action Checklist:\n"
            f"- Verify structural design load calculations and safety factors ($1.5$ for limit state of strength).\n"
            f"- Ensure mandatory testing of materials (Cube compressive testing at 7 and 28 days per IS 516).\n"
            f"- Enforce daily toolbox talks and personal protective equipment (PPE) before commencing work.\n"
            f"- Record all observations in the formal Site Quality & Safety Logbook.\n\n"
            f"*(Tip: To get real-time dynamic Gemini 2.5 multimodal reasoning, enter your Google Gemini API key in the sidebar!)*"
        )
