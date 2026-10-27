"""
Planning & Real Estate Valuation Engine (Epic 3)
Calculates project construction budgets, CapEx incurred, current market valuations in INR (Lakhs/Crores),
material quantification (Steel, Cement, Concrete) based on IS 456 & CPWD norms,
and synthesizes conceptual 3D architectural renderings via Pollinations AI.
"""

import urllib.parse
from typing import Dict, Any, List, Tuple

# Base Construction Costs per sq.ft in INR (Excluding Land Cost)
STRUCTURE_BASE_RATES = {
    "Residential High-Rise (G+24)": {
        "Economy": 1850,
        "Standard": 2400,
        "Premium": 3200,
        "Luxury": 4200,
        "steel_kg_per_sqft": 4.5,
        "cement_bags_per_sqft": 0.44,
        "rmc_cum_per_sqft": 0.042,
        "land_share_multiplier": 1.9,
    },
    "Commercial IT Park / Office Tower": {
        "Economy": 2200,
        "Standard": 2900,
        "Premium": 3800,
        "Luxury": 5100,
        "steel_kg_per_sqft": 5.2,
        "cement_bags_per_sqft": 0.48,
        "rmc_cum_per_sqft": 0.048,
        "land_share_multiplier": 2.2,
    },
    "Industrial Pre-Engineered Warehouse": {
        "Economy": 1200,
        "Standard": 1600,
        "Premium": 2100,
        "Luxury": 2800,
        "steel_kg_per_sqft": 6.8, # PEB steel structure
        "cement_bags_per_sqft": 0.28,
        "rmc_cum_per_sqft": 0.028,
        "land_share_multiplier": 1.4,
    },
    "Luxury Gated Villa / Bungalow": {
        "Economy": 2400,
        "Standard": 3100,
        "Premium": 4400,
        "Luxury": 6200,
        "steel_kg_per_sqft": 4.0,
        "cement_bags_per_sqft": 0.42,
        "rmc_cum_per_sqft": 0.038,
        "land_share_multiplier": 2.6,
    },
    "Mixed-Use Retail & Residential Tower": {
        "Economy": 2100,
        "Standard": 2750,
        "Premium": 3650,
        "Luxury": 4800,
        "steel_kg_per_sqft": 4.8,
        "cement_bags_per_sqft": 0.46,
        "rmc_cum_per_sqft": 0.045,
        "land_share_multiplier": 2.1,
    }
}

LOCATION_TIER_CONFIG = {
    "Tier 1 (Mumbai, Bengaluru, Delhi NCR, Hyderabad)": {
        "cost_multiplier": 1.25,
        "market_rate_per_sqft": 13500,
        "tier_name": "Tier 1 Metro"
    },
    "Tier 2 (Pune, Ahmedabad, Kolkata, Chennai, Jaipur)": {
        "cost_multiplier": 1.05,
        "market_rate_per_sqft": 8200,
        "tier_name": "Tier 2 Emerging"
    },
    "Tier 3 (Indore, Lucknow, Coimbatore, Nagpur, Vizag)": {
        "cost_multiplier": 0.90,
        "market_rate_per_sqft": 4800,
        "tier_name": "Tier 3 Regional"
    }
}

CONSTRUCTION_PHASES = [
    {"name": "Site Prep & Deep Excavation", "range": (0, 15), "typical_pct": 12},
    {"name": "Substructure & Piling / Foundation", "range": (15, 30), "typical_pct": 18},
    {"name": "RCC Superstructure Framing", "range": (30, 60), "typical_pct": 30},
    {"name": "Blockwork, MEP Rough-ins & Plastering", "range": (60, 80), "typical_pct": 20},
    {"name": "Architectural Finishes, Facade & Elevators", "range": (80, 95), "typical_pct": 15},
    {"name": "Testing, Commissioning & OC Handover", "range": (95, 100), "typical_pct": 5}
]


def format_inr(amount: float) -> str:
    """Formats raw INR amounts into clean Indian Lakhs and Crores."""
    if amount >= 10000000: # 1 Crore = 10,000,000
        crores = amount / 10000000
        return f"₹ {crores:.2f} Cr"
    elif amount >= 100000: # 1 Lakh = 100,000
        lakhs = amount / 100000
        return f"₹ {lakhs:.2f} Lakhs"
    else:
        return f"₹ {amount:,.0f}"


def calculate_project_metrics(
    structure_type: str,
    built_up_sqft: float,
    location_tier: str,
    grade: str,
    completion_pct: float
) -> Dict[str, Any]:
    """Calculates comprehensive financial and material metrics for construction planning."""
    
    struct_info = STRUCTURE_BASE_RATES.get(structure_type, STRUCTURE_BASE_RATES["Residential High-Rise (G+24)"])
    tier_info = LOCATION_TIER_CONFIG.get(location_tier, LOCATION_TIER_CONFIG["Tier 1 (Mumbai, Bengaluru, Delhi NCR, Hyderabad)"])
    
    base_rate = struct_info.get(grade, 2400)
    adjusted_construction_rate = base_rate * tier_info["cost_multiplier"]
    
    # 1. Total Direct Construction Budget
    total_construction_budget = built_up_sqft * adjusted_construction_rate
    
    # 2. CapEx Incurred vs Remaining
    completion_ratio = completion_pct / 100.0
    capex_incurred = total_construction_budget * completion_ratio
    capex_remaining = total_construction_budget - capex_incurred
    
    # 3. Market Asset Valuation
    # Total finished market value upon completion = Area * Market Rate per sq.ft
    finished_market_value = built_up_sqft * tier_info["market_rate_per_sqft"]
    # If standard grade is exceeded, add premium factor
    grade_multipliers = {"Economy": 0.85, "Standard": 1.0, "Premium": 1.22, "Luxury": 1.55}
    finished_market_value *= grade_multipliers.get(grade, 1.0)
    
    # Current valuation during construction:
    # Baseline land equity (~40% of finished value) + (Completion % * Construction & Developer Value-Add ~60%)
    land_equity_base = finished_market_value * 0.38
    development_progress_value = (finished_market_value - land_equity_base) * completion_ratio
    current_asset_valuation = land_equity_base + development_progress_value
    
    # 4. Material Quantification (IS 456 Thumb Rules)
    steel_tonnes = (built_up_sqft * struct_info["steel_kg_per_sqft"]) / 1000.0
    cement_bags = built_up_sqft * struct_info["cement_bags_per_sqft"]
    cement_tonnes = (cement_bags * 50.0) / 1000.0
    rmc_volume_cum = built_up_sqft * struct_info["rmc_cum_per_sqft"]
    sand_brass = (rmc_volume_cum * 0.45) / 2.83 # 1 Brass = 2.83 cu.m
    aggregate_brass = (rmc_volume_cum * 0.90) / 2.83
    
    # Materials consumed so far vs remaining
    steel_consumed = steel_tonnes * completion_ratio
    cement_consumed_bags = cement_bags * completion_ratio
    rmc_consumed_cum = rmc_volume_cum * completion_ratio
    
    # 5. Cost Breakdown by Discipline
    trade_breakdown = {
        "Civil & Structural RCC (42%)": total_construction_budget * 0.42,
        "Finishes, Facade & Glazing (23%)": total_construction_budget * 0.23,
        "MEP (Electrical, HVAC, Plumbing, Fire) (19%)": total_construction_budget * 0.19,
        "Approvals, Permits & Architecture (9%)": total_construction_budget * 0.09,
        "Contingency & Escalation Reserve (7%)": total_construction_budget * 0.07,
    }
    
    # 6. Current Phase Identification
    current_phase = "Site Preparation"
    for phase in CONSTRUCTION_PHASES:
        p_min, p_max = phase["range"]
        if p_min <= completion_pct <= p_max:
            current_phase = phase["name"]
            break
            
    return {
        "structure_type": structure_type,
        "built_up_sqft": built_up_sqft,
        "location_tier": location_tier,
        "grade": grade,
        "completion_pct": completion_pct,
        "current_phase": current_phase,
        "construction_rate_per_sqft": adjusted_construction_rate,
        "total_budget_inr": total_construction_budget,
        "total_budget_fmt": format_inr(total_construction_budget),
        "capex_incurred_inr": capex_incurred,
        "capex_incurred_fmt": format_inr(capex_incurred),
        "capex_remaining_inr": capex_remaining,
        "capex_remaining_fmt": format_inr(capex_remaining),
        "current_valuation_inr": current_asset_valuation,
        "current_valuation_fmt": format_inr(current_asset_valuation),
        "finished_market_value_inr": finished_market_value,
        "finished_market_value_fmt": format_inr(finished_market_value),
        "materials": {
            "steel_total_tonnes": round(steel_tonnes, 1),
            "steel_consumed_tonnes": round(steel_consumed, 1),
            "cement_total_bags": int(cement_bags),
            "cement_consumed_bags": int(cement_consumed_bags),
            "cement_total_tonnes": round(cement_tonnes, 1),
            "rmc_total_cum": round(rmc_volume_cum, 1),
            "rmc_consumed_cum": round(rmc_consumed_cum, 1),
            "sand_brass": round(sand_brass, 1),
            "aggregate_brass": round(aggregate_brass, 1)
        },
        "trade_breakdown": trade_breakdown
    }


def generate_architectural_render_url(
    structure_type: str,
    grade: str,
    location_tier: str,
    custom_style: str = "Modern Biophilic",
    seed: int = 42
) -> Tuple[str, str]:
    """
    Synthesizes an architectural visualization prompt and builds a Pollinations AI / Flux URL.
    Returns: (image_url, prompt_text)
    """
    clean_struct = structure_type.split("(")[0].strip()
    
    style_prompts = {
        "Modern Biophilic": "lush vertical sky gardens, cantilevered balconies with indigenous foliage, warm timber louvers, floor-to-ceiling double-glazed low-E glass",
        "Brutalist High-Tech": "exposed architectural fair-faced concrete, geometric aerodynamic steel trusses, recessed strip LED illumination, dramatic shadows",
        "Contemporary Glass Facade": "curtain wall facade with fritted reflective glass, ultra-sleek composite aluminum cladding, luminous interior double-height atrium",
        "Heritage Indo-Modern": "carved sandstone jali lattice screens, ambient courtyard water bodies, warm terracotta accents, modern structural minimalism",
        "Industrial Logistics Hub": "high-bay structural steel portal frames, polished concrete hardstand aprons, dock levelers, solar PV rooftop array, twilight ambient lighting"
    }
    
    style_desc = style_prompts.get(custom_style, style_prompts["Modern Biophilic"])
    
    prompt = (
        f"Award-winning architectural visualization of a {grade.lower()} {clean_struct}, "
        f"{style_desc}, situated in an upscale {location_tier.split('(')[0].strip()} metropolis. "
        f"Professional architectural photography, golden hour ambient lighting, dramatic perspective view, "
        f"hyperrealistic 8k, Octane render style, photorealistic textures, HDR, perfectly balanced composition, "
        f"crisp details, unreal engine 5 architectural showcase"
    )
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=640&nologo=true&seed={seed}&model=flux"
    
    return url, prompt
