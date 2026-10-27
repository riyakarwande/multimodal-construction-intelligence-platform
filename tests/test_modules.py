"""
Automated Unit and Integration Tests for Multimodal Construction Intelligence Platform.
Verifies all modules, data contracts, calculations, and fallback mechanisms.
"""

import os
import unittest
from PIL import Image

from modules.sample_generator import generate_sample_assets
from modules.gemini_client import GeminiEngine, extract_json_from_text
from modules.safety_audit import (
    generate_mock_safety_audit,
    format_ppe_checklist_markdown,
    SAFETY_SYSTEM_PROMPT,
    SAFETY_USER_PROMPT
)
from modules.crack_diagnostics import (
    generate_mock_crack_diagnostics,
    CRACK_SYSTEM_PROMPT,
    CRACK_USER_PROMPT
)
from modules.valuation_planner import (
    calculate_project_metrics,
    generate_architectural_render_url,
    format_inr,
    STRUCTURE_BASE_RATES,
    LOCATION_TIER_CONFIG
)
from modules.weather_assistant import (
    WEATHER_PROTOCOLS,
    get_fallback_engineering_response
)


class TestConstructionPlatform(unittest.TestCase):

    def setUp(self):
        self.assets = generate_sample_assets("assets")
        self.engine = GeminiEngine(api_key=None)  # Test deterministic demo engine

    def test_sample_assets_generated(self):
        """Verify that all sample schematic assets exist and are readable images."""
        for key, path in self.assets.items():
            self.assertTrue(os.path.exists(path), f"Asset {key} at {path} should exist")
            with Image.open(path) as img:
                self.assertEqual(img.size, (800, 600), f"Asset {key} should be 800x600")

    def test_json_extractor(self):
        """Verify robust JSON extraction from text and markdown code fences."""
        raw_json_str = '{"safety_score": 85, "status": "Compliant"}'
        md_json_str = f"```json\n{raw_json_str}\n```"
        
        parsed1 = extract_json_from_text(raw_json_str)
        self.assertIsNotNone(parsed1)
        self.assertEqual(parsed1["safety_score"], 85)
        
        parsed2 = extract_json_from_text(md_json_str)
        self.assertIsNotNone(parsed2)
        self.assertEqual(parsed2["safety_score"], 85)

    def test_safety_audit_contract(self):
        """Verify Tab 1 PPE Safety Audit JSON contract schema."""
        hazard_audit = generate_mock_safety_audit("scaffold_hazard")
        self.assertIn("safety_score", hazard_audit)
        self.assertIn("overall_status", hazard_audit)
        self.assertIn("ppe_detection", hazard_audit)
        self.assertIn("identified_hazards", hazard_audit)
        
        self.assertIsInstance(hazard_audit["safety_score"], int)
        self.assertTrue(0 <= hazard_audit["safety_score"] <= 100)
        
        # Check PPE items
        ppe = hazard_audit["ppe_detection"]
        self.assertIn("helmets", ppe)
        self.assertIn("high_vis_vests", ppe)
        self.assertIn("steel_toe_boots", ppe)
        self.assertIn("safety_harnesses", ppe)
        
        # Check markdown formatter
        md_table = format_ppe_checklist_markdown(ppe)
        self.assertIn("Safety Helmets", md_table)
        self.assertIn("Fall Arrest Harness", md_table)

    def test_crack_diagnostics_contract(self):
        """Verify Tab 2 Crack Diagnostics classification and IS 456 limits."""
        for defect in ["shear", "hairline", "spalling"]:
            diag = generate_mock_crack_diagnostics(defect)
            self.assertIn("defect_type", diag)
            self.assertIn("estimated_crack_width_mm", diag)
            self.assertIn("severity_score", diag)
            self.assertIn("is_456_compliance", diag)
            self.assertIn("recommended_engineering_repairs", diag)
            
            self.assertGreater(len(diag["recommended_engineering_repairs"]), 0)
            self.assertTrue(0 <= diag["severity_score"] <= 100)

    def test_valuation_planner_calculations(self):
        """Verify Tab 3 CapEx and real estate valuation math."""
        metrics = calculate_project_metrics(
            structure_type="Residential High-Rise (G+24)",
            built_up_sqft=100000,
            location_tier="Tier 1 (Mumbai, Bengaluru, Delhi NCR, Hyderabad)",
            grade="Premium",
            completion_pct=50
        )
        
        self.assertIn("total_budget_inr", metrics)
        self.assertIn("capex_incurred_inr", metrics)
        self.assertIn("capex_remaining_inr", metrics)
        self.assertIn("current_valuation_inr", metrics)
        self.assertIn("materials", metrics)
        
        # Check math consistency: 50% completion means incurred is exactly half of total
        self.assertAlmostEqual(metrics["capex_incurred_inr"], metrics["total_budget_inr"] * 0.5, places=2)
        self.assertAlmostEqual(metrics["capex_remaining_inr"], metrics["total_budget_inr"] * 0.5, places=2)
        
        # Check material quantification exists
        mats = metrics["materials"]
        self.assertGreater(mats["steel_total_tonnes"], 0)
        self.assertGreater(mats["cement_total_bags"], 0)
        self.assertGreater(mats["rmc_total_cum"], 0)

    def test_architectural_render_url(self):
        """Verify Pollinations AI URL generation."""
        url, prompt = generate_architectural_render_url(
            structure_type="Commercial IT Park / Office Tower",
            grade="Luxury",
            location_tier="Tier 1 (Mumbai, Bengaluru, Delhi NCR, Hyderabad)",
            custom_style="Contemporary Glass Facade",
            seed=1234
        )
        self.assertTrue(url.startswith("https://image.pollinations.ai/prompt/"))
        self.assertIn("seed=1234", url)
        self.assertIn("Commercial IT Park", prompt)

    def test_weather_protocols_and_chatbot(self):
        """Verify Tab 4 weather matrices and chatbot fallback."""
        for condition, proto in WEATHER_PROTOCOLS.items():
            self.assertIn("crane_status", proto)
            self.assertIn("height_status", proto)
            self.assertIn("concrete_protocol", proto)
            self.assertIn("electrical_safety", proto)
            
        resp = get_fallback_engineering_response("curing intervals for M25")
        self.assertIn("IS 456", resp)
        self.assertIn("curing", resp.lower())


if __name__ == "__main__":
    unittest.main()
