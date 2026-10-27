"""
Multimodal Construction Intelligence Platform
Category: Generative AI | Real Estate Decision Support | Platform ID: 6ac4c98d1dcde6d7857c1642
Skill Wallet Capstone Project 1 - Turnkey Production Application

Powered by Streamlit, Gemini 2.5 / 1.5 Multimodal Vision, Plotly, and Pollinations AI.
"""

import os
import io
import json
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px

# Import custom modules
from modules.gemini_client import GeminiEngine
from modules.safety_audit import (
    SAFETY_SYSTEM_PROMPT,
    SAFETY_USER_PROMPT,
    generate_mock_safety_audit,
    format_ppe_checklist_markdown
)
from modules.crack_diagnostics import (
    CRACK_SYSTEM_PROMPT,
    CRACK_USER_PROMPT,
    generate_mock_crack_diagnostics
)
from modules.valuation_planner import (
    STRUCTURE_BASE_RATES,
    LOCATION_TIER_CONFIG,
    CONSTRUCTION_PHASES,
    calculate_project_metrics,
    generate_architectural_render_url,
    format_inr
)
from modules.weather_assistant import (
    WEATHER_PROTOCOLS,
    SITE_ENGINEER_CHAT_SYSTEM_PROMPT,
    get_fallback_engineering_response
)
from modules.sample_generator import generate_sample_assets

# Page Configuration
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure sample assets exist
SAMPLE_ASSETS = generate_sample_assets("assets")

# Custom Modern Industrial CSS Styling
st.markdown("""
<style>
    /* Global Styles */
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    .main-title {
        color: #F8FAFC;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .main-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        font-weight: 400;
    }
    .badge-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 14px;
    }
    .custom-badge {
        background: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.4px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .custom-badge-cyan {
        background: rgba(6, 182, 212, 0.15);
        color: #22D3EE;
        border: 1px solid rgba(6, 182, 212, 0.4);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .custom-badge-green {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* Card Styles */
    .metric-card {
        background: #1E293B;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 10px;
        padding: 18px 20px;
        margin-bottom: 15px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: rgba(245, 158, 11, 0.5);
    }
    .card-title {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .card-value {
        color: #F8FAFC;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .card-caption {
        color: #64748B;
        font-size: 0.8rem;
        margin-top: 4px;
    }
    
    /* Severity Pills */
    .pill-critical {
        background: #DC2626;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .pill-high {
        background: #EA580C;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .pill-medium {
        background: #D97706;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .pill-low {
        background: #2563EB;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .pill-compliant {
        background: #059669;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    
    /* Chat bubbles */
    .stChatMessage {
        border-radius: 10px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# SIDEBAR: Configuration, Architecture Overview & Platform Info
# -------------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1541888946425-d0fbb186c5f7?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.markdown("### 🏗️ Platform Control Center")
    st.caption("Multimodal AI Decision Support Engine")
    
    st.divider()
    
    # Secure API Key Input
    st.markdown("#### 🔑 Multimodal LLM Credentials")
    gemini_key_input = st.text_input(
        "Google Gemini API Key",
        value=os.environ.get("GEMINI_API_KEY", ""),
        type="password",
        help="Enter Google Gemini API Key for live vision and chat reasoning. Leave blank for automated Demonstration Mode."
    )
    
    selected_model = st.selectbox(
        "Preferred Vision Model",
        ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0
    )
    
    # Initialize Engine
    engine = GeminiEngine(api_key=gemini_key_input, preferred_model=selected_model)
    
    if engine.is_live_ready:
        st.success("🟢 **Live Multimodal Mode Active** (Gemini API Connected)")
    else:
        st.info("🟡 **Demonstration Mode Active** (High-Fidelity Deterministic Models)")
        st.caption("No key supplied. All modules will run using calibrated engineering simulation models.")
        
    st.divider()
    
    # Platform Metadata & Architecture Info
    st.markdown("#### 📋 Platform Metadata")
    st.markdown("""
    - **Platform ID:** `6ac4c98d1dcde6d7857c1642`
    - **Category:** Generative AI | Real Estate Decision Support
    - **Standards:** OSHA 1926, IS 456:2000, ACI 224R
    - **Deployment:** Streamlit Cloud Zero-DB Ready
    """)
    
    with st.expander("📌 Kanban Epics Coverage", expanded=False):
        st.markdown("""
        - **Prerequisites:** Python 3.9+, Streamlit, Pillow
        - **Epic 1:** Requirements, Env & Graceful Fallback
        - **Epic 2:** PPE Safety Vision & Crack Diagnostics
        - **Epic 3:** Project Planning & Real Estate Valuation
        - **Epic 4:** Multimodal AI & JSON Data Contracts
        - **Epic 5:** Site Chatbot & Weather Advisory
        - **Epic 6:** Executive Interface & Cloud Deployment
        """)
        
    st.divider()
    if st.button("🧹 Clear Chat & Reset Session", use_container_width=True):
        st.session_state.pop("chat_history", None)
        st.session_state.pop("safety_audit_result", None)
        st.session_state.pop("crack_result", None)
        st.success("Session state refreshed.")
        st.rerun()

# -------------------------------------------------------------
# MAIN HEADER & BADGES
# -------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <div class="main-title">
        <span>🏗️ Multimodal Construction Intelligence Platform</span>
    </div>
    <div class="main-subtitle">
        Intelligent Decision-Support System: Computer Vision Safety Audits, Concrete Diagnostics, CapEx & Valuation Modeling, and Weather Protocols.
    </div>
    <div class="badge-bar">
        <span class="custom-badge">ID: 6ac4c98d1dcde6d7857c1642</span>
        <span class="custom-badge-cyan">OSHA 1926 & IS 456 Standards</span>
        <span class="custom-badge-green">Streamlit Cloud Ready</span>
        <span class="custom-badge">Multimodal Vision LLM</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# APPLICATION TABS (EPIC 2, EPIC 3, EPIC 5)
# -------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 Tab 1: Site Safety & PPE Audit",
    "🔍 Tab 2: Crack Diagnostics & Structural Integrity",
    "📊 Tab 3: Planning & Real Estate Valuation",
    "🌦️ Tab 4: Daily Site Assistant & Weather Advisory"
])

# =============================================================
# TAB 1: SITE SAFETY & PPE AUDIT (EPIC 2)
# =============================================================
with tab1:
    st.markdown("### 🦺 Site Safety & Worker PPE Compliance Audit (OSHA 1926 / IS 456)")
    st.caption("Upload site photographs or select curated CCTV feeds to inspect worker PPE compliance, detect life-critical hazards, and generate structured audit reports.")
    
    col_input, col_preview = st.columns([1, 1], gap="medium")
    
    with col_input:
        st.markdown("#### 1. Select Inspection Source")
        safety_source_mode = st.radio(
            "Source Selection",
            ["Curated Sample CCTV Feeds (Instant Test)", "Upload Custom Site Photo (JPG/PNG)"],
            horizontal=True,
            key="safety_source_radio"
        )
        
        selected_safety_image = None
        sample_safety_type = "scaffold_hazard"
        
        if safety_source_mode == "Curated Sample CCTV Feeds (Instant Test)":
            sample_choice = st.selectbox(
                "Choose Inspection Scenario",
                [
                    "Sample A: Scaffolding Hazard (Missing Harness & Hardhat - Level 3)",
                    "Sample B: Rebar Trench Fabrication (100% Compliant Crew)"
                ]
            )
            if "Sample A" in sample_choice:
                sample_path = SAMPLE_ASSETS["ppe_hazard"]
                sample_safety_type = "scaffold_hazard"
            else:
                sample_path = SAMPLE_ASSETS["ppe_compliant"]
                sample_safety_type = "compliant"
                
            selected_safety_image = Image.open(sample_path)
        else:
            uploaded_safety_file = st.file_uploader(
                "Upload Site Photo",
                type=["jpg", "jpeg", "png"],
                help="Upload a clear photograph of construction activity.",
                key="safety_file_uploader"
            )
            if uploaded_safety_file:
                selected_safety_image = Image.open(uploaded_safety_file)
                
        run_safety_audit = st.button(
            "⚡ Execute Multimodal Safety Audit",
            type="primary",
            use_container_width=True,
            disabled=(selected_safety_image is None)
        )
        
    with col_preview:
        st.markdown("#### 2. Photographic Evidence Feed")
        if selected_safety_image:
            st.image(selected_safety_image, caption="Active Site Inspection Frame", use_container_width=True)
        else:
            st.info("Please select or upload a site photograph to begin.")
            
    # Audit Execution
    if run_safety_audit and selected_safety_image:
        with st.spinner("Analyzing site imagery against OSHA 1926 and IS 456 safety codes..."):
            audit_result, is_live, msg = engine.analyze_image_multimodal(
                image_input=selected_safety_image,
                prompt=SAFETY_USER_PROMPT,
                system_instruction=SAFETY_SYSTEM_PROMPT,
                fallback_data_generator=lambda: generate_mock_safety_audit(sample_safety_type)
            )
            st.session_state["safety_audit_result"] = audit_result
            st.session_state["safety_is_live"] = is_live
            st.session_state["safety_msg"] = msg

    # Display Results
    if "safety_audit_result" in st.session_state:
        res = st.session_state["safety_audit_result"]
        is_live = st.session_state.get("safety_is_live", False)
        
        st.divider()
        if is_live:
            st.success("🟢 **Live Gemini Vision Analysis Completed**")
        else:
            st.info("🟡 **Demonstration Mode Results** (Pre-calibrated forensic safety benchmark)")
            
        # Top KPI Metrics Row
        score = res.get("safety_score", 0)
        overall_status = res.get("overall_status", "Unknown")
        worker_count = res.get("worker_count_estimate", 0)
        hazards = res.get("identified_hazards", [])
        critical_count = sum(1 for h in hazards if h.get("severity") == "Critical")
        
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="card-title">Overall Safety Score</div>
                <div class="card-value" style="color: {'#10B981' if score>=80 else '#F59E0B' if score>=60 else '#EF4444'};">
                    {score} / 100
                </div>
                <div class="card-caption">OSHA Weighted Compliance</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi2:
            status_color = "#10B981" if "compliant" in overall_status.lower() else "#F59E0B" if "conditional" in overall_status.lower() else "#EF4444"
            st.markdown(f"""
            <div class="metric-card">
                <div class="card-title">Audit Status</div>
                <div class="card-value" style="font-size: 1.3rem; color: {status_color};">
                    {overall_status}
                </div>
                <div class="card-caption">Site Permit Authorization</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="card-title">Workers Detected</div>
                <div class="card-value" style="color: #38BDF8;">
                    {worker_count} Operatives
                </div>
                <div class="card-caption">In Active Visual Zone</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="card-title">Critical Hazards</div>
                <div class="card-value" style="color: {'#EF4444' if critical_count>0 else '#10B981'};">
                    {critical_count} Violations
                </div>
                <div class="card-caption">Immediate Remedies Required</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Detail Visualizations: PPE Compliance Radar/Bar & Table
        col_chart, col_ppe_table = st.columns([1, 1], gap="medium")
        
        with col_chart:
            st.markdown("#### 📊 PPE Compliance Distribution")
            ppe_data = res.get("ppe_detection", {})
            categories = []
            rates = []
            
            for item_name, details in ppe_data.items():
                clean_name = item_name.replace("_", " ").title()
                rate_str = details.get("compliance_rate", "0%")
                try:
                    num_rate = float(rate_str.replace("%", "").strip())
                except ValueError:
                    num_rate = 100.0 if details.get("detected") else 0.0
                categories.append(clean_name)
                rates.append(num_rate)
                
            if categories:
                fig = go.Figure(go.Bar(
                    x=rates,
                    y=categories,
                    orientation='h',
                    marker=dict(
                        color=rates,
                        colorscale=[[0, '#EF4444'], [0.5, '#F59E0B'], [1, '#10B981']],
                        showscale=False
                    ),
                    text=[f"{r:.0f}%" for r in rates],
                    textposition='auto',
                ))
                fig.update_layout(
                    margin=dict(l=20, r=20, t=20, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(range=[0, 105], showgrid=True, gridcolor='#334155', ticksuffix="%"),
                    yaxis=dict(showgrid=False, autorange="reversed"),
                    font=dict(color="#F8FAFC"),
                    height=260
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numerical PPE distribution data available.")
                
        with col_ppe_table:
            st.markdown("#### 📋 PPE Detection Checklist")
            st.markdown(format_ppe_checklist_markdown(ppe_data))
            
        # Identified Hazards & Corrective Remedies
        st.markdown("#### 🚨 Identified Site Hazards & Engineering Remedies")
        if hazards:
            for idx, h in enumerate(hazards, 1):
                sev = h.get("severity", "Medium")
                pill_class = f"pill-{sev.lower()}" if sev.lower() in ["critical", "high", "medium", "low"] else "pill-medium"
                
                with st.container():
                    st.markdown(f"""
                    <div style="background: #1E293B; border-left: 4px solid {'#EF4444' if sev=='Critical' else '#F59E0B' if sev=='High' else '#3B82F6'}; border-radius: 6px; padding: 14px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <strong style="font-size: 1.05rem; color: #F8FAFC;">#{idx}: {h.get('hazard')}</strong>
                            <span class="{pill_class}">{sev.upper()}</span>
                        </div>
                        <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 6px;">
                            📍 <b>Location:</b> {h.get('location', 'Site Wide')} &nbsp;|&nbsp; 📜 <b>Standard:</b> {h.get('standard_violated', 'OSHA 1926')}
                        </div>
                        <div style="background: rgba(15, 23, 42, 0.6); padding: 8px 12px; border-radius: 4px; font-size: 0.88rem; color: #E2E8F0;">
                            <b>🛠️ Corrective Remedy:</b> {h.get('corrective_remedy')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("🎉 No active site safety violations detected! Site is operating under compliance.")
            
        # Audit Summary & Action Directives
        summary_text = res.get("audit_summary", "Audit completed.")
        st.info(f"**Chief Safety Officer Directive:** {summary_text}")
        
        # Downloadable JSON Contract
        st.download_button(
            label="📥 Download Structured JSON Safety Report",
            data=json.dumps(res, indent=2),
            file_name="site_safety_ppe_audit_report.json",
            mime="application/json",
            use_container_width=True
        )
        
        with st.expander("👁️ View Raw JSON Data Contract", expanded=False):
            st.json(res)


# =============================================================
# TAB 2: CRACK DIAGNOSTICS & STRUCTURAL INTEGRITY (EPIC 2)
# =============================================================
with tab2:
    st.markdown("### 🔍 Concrete Crack Diagnostics & Structural Integrity (IS 456 / ACI 224R)")
    st.caption("Forensic multimodal classification of concrete defects: Hairline Crazing, Settlement Cracks, Structural Shear, Thermal Expansion, and Spalling with rebar corrosion.")
    
    col_c_in, col_c_prev = st.columns([1, 1], gap="medium")
    
    with col_c_in:
        st.markdown("#### 1. Select Concrete Surface Source")
        crack_source_mode = st.radio(
            "Source Selection",
            ["Curated Forensic Defect Samples (Instant Test)", "Upload Custom Concrete Surface Photo (JPG/PNG)"],
            horizontal=True,
            key="crack_source_radio"
        )
        
        selected_crack_image = None
        sample_crack_hint = "shear"
        
        if crack_source_mode == "Curated Forensic Defect Samples (Instant Test)":
            crack_sample_choice = st.selectbox(
                "Choose Structural Defect Type",
                [
                    "Sample 1: Structural Shear Crack (RCC Beam B-104, 45° Diagonal)",
                    "Sample 2: Hairline Shrinkage Crazing (Plaster / Early Stage)",
                    "Sample 3: Spalling & Delamination (Exposed Corroded Rebar)"
                ]
            )
            if "Sample 1" in crack_sample_choice:
                sample_crack_path = SAMPLE_ASSETS["shear_crack"]
                sample_crack_hint = "shear"
            elif "Sample 2" in crack_sample_choice:
                sample_crack_path = SAMPLE_ASSETS["hairline_crack"]
                sample_crack_hint = "hairline"
            else:
                sample_crack_path = SAMPLE_ASSETS["spalling_crack"]
                sample_crack_hint = "spalling"
                
            selected_crack_image = Image.open(sample_crack_path)
        else:
            uploaded_crack_file = st.file_uploader(
                "Upload Concrete / Wall Photo",
                type=["jpg", "jpeg", "png"],
                help="Upload a high-resolution photo of the concrete crack or surface defect.",
                key="crack_file_uploader"
            )
            if uploaded_crack_file:
                selected_crack_image = Image.open(uploaded_crack_file)
                
        run_crack_diagnostics = st.button(
            "🔍 Execute Crack Classification & Diagnostics",
            type="primary",
            use_container_width=True,
            disabled=(selected_crack_image is None)
        )
        
    with col_c_prev:
        st.markdown("#### 2. Surface Inspection Frame")
        if selected_crack_image:
            st.image(selected_crack_image, caption="Concrete Surface Specimen", use_container_width=True)
        else:
            st.info("Select or upload a concrete surface photo to begin analysis.")
            
    # Diagnostic Execution
    if run_crack_diagnostics and selected_crack_image:
        with st.spinner("Classifying defect type and calculating IS 456 permissible crack width limits..."):
            crack_result, is_live, msg = engine.analyze_image_multimodal(
                image_input=selected_crack_image,
                prompt=CRACK_USER_PROMPT,
                system_instruction=CRACK_SYSTEM_PROMPT,
                fallback_data_generator=lambda: generate_mock_crack_diagnostics(sample_crack_hint)
            )
            st.session_state["crack_result"] = crack_result
            st.session_state["crack_is_live"] = is_live
            st.session_state["crack_msg"] = msg

    # Display Diagnostic Results
    if "crack_result" in st.session_state:
        c_res = st.session_state["crack_result"]
        c_is_live = st.session_state.get("crack_is_live", False)
        
        st.divider()
        if c_is_live:
            st.success("🟢 **Live Multimodal Crack Diagnostics Completed**")
        else:
            st.info("🟡 **Demonstration Mode Structural Diagnostics** (Calibrated forensic finite element model)")
            
        defect_type = c_res.get("defect_type", "Structural Crack")
        crack_width = c_res.get("estimated_crack_width_mm", 0.0)
        c_severity = c_res.get("severity_score", 0)
        risk_level = c_res.get("structural_risk_level", "Moderate")
        urgency = c_res.get("urgency", "Priority")
        is_456 = c_res.get("is_456_compliance", {})
        
        # Metric Cards Row
        cm1, cm2, cm3, cm4 = st.columns(4)
        
        with cm1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="card-title">Defect Classification</div>
                <div class="card-value" style="font-size: 1.25rem; color: #F59E0B;">
                    {defect_type}
                </div>
                <div class="card-caption">Forensic Defect Category</div>
            </div>
            """, unsafe_allow_html=True)
            
        with cm2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="card-title">Estimated Crack Width</div>
                <div class="card-value" style="color: {'#EF4444' if crack_width>0.3 else '#10B981'};">
                    {crack_width:.2f} mm
                </div>
                <div class="card-caption">IS 456 Limit: 0.30 mm (Mild)</div>
            </div>
            """, unsafe_allow_html=True)
            
        with cm3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="card-title">Structural Risk Rating</div>
                <div class="card-value" style="color: {'#EF4444' if risk_level=='Critical' else '#F59E0B' if risk_level=='High' else '#10B981'};">
                    {risk_level} ({c_severity}/100)
                </div>
                <div class="card-caption">Capacity Degradation Score</div>
            </div>
            """, unsafe_allow_html=True)
            
        with cm4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="card-title">Repair Urgency</div>
                <div class="card-value" style="font-size: 1.15rem; color: {'#EF4444' if 'Immediate' in urgency else '#F59E0B'};">
                    {urgency}
                </div>
                <div class="card-caption">Recommended Action Window</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Gauge & Root Causes Row
        col_gauge, col_root = st.columns([1, 1], gap="medium")
        
        with col_gauge:
            st.markdown("#### 📏 Crack Width vs IS 456 Limit Gauge")
            max_gauge = max(5.0, crack_width * 1.3)
            gauge_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=crack_width,
                number={'suffix': " mm", 'font': {'color': '#F8FAFC'}},
                gauge={
                    'axis': {'range': [0, max_gauge], 'tickcolor': '#94A3B8'},
                    'bar': {'color': "#EF4444" if crack_width > 0.3 else "#10B981"},
                    'steps': [
                        {'range': [0, 0.10], 'color': "rgba(16, 185, 129, 0.3)"},
                        {'range': [0.10, 0.30], 'color': "rgba(245, 158, 11, 0.3)"},
                        {'range': [0.30, max_gauge], 'color': "rgba(239, 68, 68, 0.35)"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 0.30
                    }
                }
            ))
            gauge_fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=30, b=20),
                height=220
            )
            st.plotly_chart(gauge_fig, use_container_width=True)
            st.caption(f"**IS 456 Verdict:** {is_456.get('compliance_verdict', 'Evaluated')}")
            
        with col_root:
            st.markdown("#### 🔬 Root Cause Analysis")
            roots = c_res.get("root_causes", [])
            for r_idx, root in enumerate(roots, 1):
                st.markdown(f"- **Trigger {r_idx}:** {root}")
                
            aff = c_res.get("affected_elements", [])
            if aff:
                st.markdown(f"**Affected Structural Members:** {', '.join(aff)}")
                
        # Recommended Engineering Repairs (Step-by-Step)
        st.markdown("#### 🛠️ Recommended Engineering Repairs & Rehabilitation Roadmap")
        repairs = c_res.get("recommended_engineering_repairs", [])
        if repairs:
            for rep in repairs:
                step_num = rep.get("step", 1)
                st.markdown(f"""
                <div style="background: #1E293B; border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 8px; padding: 14px 18px; margin-bottom: 10px;">
                    <div style="color: #F59E0B; font-weight: 700; font-size: 0.95rem; margin-bottom: 4px;">
                        PHASE {step_num}: {rep.get('method')}
                    </div>
                    <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 6px;">
                        <b>Specification:</b> <code>{rep.get('specification')}</code>
                    </div>
                    <div style="font-size: 0.88rem; color: #E2E8F0;">
                        {rep.get('procedure')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        summary = c_res.get("engineering_summary", "")
        st.info(f"**Structural Engineer Opinion:** {summary}")
        
        # Downloadable Diagnostic Report
        st.download_button(
            label="📥 Download Structured JSON Diagnostics Report",
            data=json.dumps(c_res, indent=2),
            file_name="structural_crack_diagnostic_report.json",
            mime="application/json",
            use_container_width=True
        )
        
        with st.expander("👁️ View Raw Diagnostic JSON Data Contract", expanded=False):
            st.json(c_res)


# =============================================================
# TAB 3: PLANNING & REAL ESTATE VALUATION (EPIC 3)
# =============================================================
with tab3:
    st.markdown("### 📊 Construction Planning, Material Estimation & Real Estate Valuation (INR)")
    st.caption("Parametric construction budgeting, CapEx incurred analysis, current market asset valuation in INR Lakhs & Crores, steel/cement quantification, and Pollinations AI 3D architectural rendering.")
    
    col_v1, col_v2 = st.columns([1, 1], gap="large")
    
    with col_v1:
        st.markdown("#### 1. Project Specifications")
        v_structure_type = st.selectbox(
            "Structure Classification",
            list(STRUCTURE_BASE_RATES.keys()),
            index=0
        )
        
        v_built_up_sqft = st.number_input(
            "Total Built-up Area (Sq.Ft.)",
            min_value=1000,
            max_value=2000000,
            value=75000,
            step=5000
        )
        
        v_location_tier = st.selectbox(
            "Location Tier (Indian Market)",
            list(LOCATION_TIER_CONFIG.keys()),
            index=0
        )
        
        v_grade = st.select_slider(
            "Construction Specification Grade",
            options=["Economy", "Standard", "Premium", "Luxury"],
            value="Premium"
        )
        
        v_completion_pct = st.slider(
            "Construction Milestone Progress (%)",
            min_value=0,
            max_value=100,
            value=45,
            format="%d%%"
        )
        
    # Calculate Project Metrics
    metrics = calculate_project_metrics(
        structure_type=v_structure_type,
        built_up_sqft=float(v_built_up_sqft),
        location_tier=v_location_tier,
        grade=v_grade,
        completion_pct=float(v_completion_pct)
    )
    
    with col_v2:
        st.markdown("#### 2. Milestone Progress & Current Phase")
        st.markdown(f"**Current Active Phase:** `{metrics['current_phase']}`")
        st.progress(v_completion_pct / 100.0)
        
        # Display Phase Ranges
        phase_cols = st.columns(3)
        with phase_cols[0]:
            st.caption("Foundation: 0-30%")
        with phase_cols[1]:
            st.caption("Superstructure: 30-60%")
        with phase_cols[2]:
            st.caption("Finishes & Handover: 60-100%")
            
        st.markdown(f"""
        <div style="background: #1E293B; border-radius: 8px; padding: 14px; margin-top: 10px;">
            <div style="font-size: 0.85rem; color: #94A3B8;">UNIT BASE RATE (TIER ADJUSTED)</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #F59E0B;">₹ {metrics['construction_rate_per_sqft']:,.0f} / sq.ft</div>
            <div style="font-size: 0.8rem; color: #64748B;">Includes structural, facade, MEP, contractor margin, and contingency.</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # Financial Valuation KPI Row
    st.markdown("#### 💰 Financial Valuation & Capital Expenditure (INR)")
    f1, f2, f3, f4 = st.columns(4)
    
    with f1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="card-title">Total Project Budget</div>
            <div class="card-value" style="color: #38BDF8;">
                {metrics['total_budget_fmt']}
            </div>
            <div class="card-caption">Total Direct Construction Cost</div>
        </div>
        """, unsafe_allow_html=True)
        
    with f2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="card-title">CapEx Incurred to Date</div>
            <div class="card-value" style="color: #F59E0B;">
                {metrics['capex_incurred_fmt']}
            </div>
            <div class="card-caption">{v_completion_pct}% Capital Expended</div>
        </div>
        """, unsafe_allow_html=True)
        
    with f3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="card-title">Remaining CapEx</div>
            <div class="card-value" style="color: #94A3B8;">
                {metrics['capex_remaining_fmt']}
            </div>
            <div class="card-caption">Balance to Handover</div>
        </div>
        """, unsafe_allow_html=True)
        
    with f4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="card-title">Current Asset Valuation</div>
            <div class="card-value" style="color: #10B981;">
                {metrics['current_valuation_fmt']}
            </div>
            <div class="card-caption">Finished Value: {metrics['finished_market_value_fmt']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Cost Breakdown Donut & Material Estimation
    col_donut, col_materials = st.columns([1, 1], gap="medium")
    
    with col_donut:
        st.markdown("#### 📊 Trade Cost Distribution")
        trade_names = list(metrics['trade_breakdown'].keys())
        trade_vals = list(metrics['trade_breakdown'].values())
        
        donut_fig = go.Figure(data=[go.Pie(
            labels=trade_names,
            values=trade_vals,
            hole=.45,
            marker=dict(colors=['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899']),
            textinfo='label+percent',
            showlegend=False
        )])
        donut_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10),
            height=280,
            font=dict(color="#F8FAFC")
        )
        st.plotly_chart(donut_fig, use_container_width=True)
        
    with col_materials:
        st.markdown("#### 🏗️ Material Requirements (IS 456 Thumb Rules)")
        mats = metrics['materials']
        
        st.markdown(f"""
        | Material Specification | Total Required | Consumed to Date | Unit |
        | :--- | :---: | :---: | :---: |
        | **TMT Fe 500D Reinforcement Steel** | `{mats['steel_total_tonnes']:,}` | `{mats['steel_consumed_tonnes']:,}` | Metric Tonnes |
        | **Portland Cement (OPC 53 / PPC)** | `{mats['cement_total_bags']:,}` | `{mats['cement_consumed_bags']:,}` | 50kg Bags ({mats['cement_total_tonnes']} MT) |
        | **Ready-Mix Concrete (M25/M35)** | `{mats['rmc_total_cum']:,}` | `{mats['rmc_consumed_cum']:,}` | $m^3$ (Cubic Meters) |
        | **Manufactured / River Sand** | `{mats['sand_brass']:,}` | — | Brass (100 cu.ft) |
        | **Coarse Aggregates (10/20mm)** | `{mats['aggregate_brass']:,}` | — | Brass (100 cu.ft) |
        """)
        
    st.divider()
    
    # Conceptual 3D Architectural Rendering via Pollinations AI
    st.markdown("#### 🎨 Conceptual 3D Architectural Rendering (Pollinations AI / Flux)")
    st.caption("Dynamically synthesizes photorealistic architectural visualizations using state-of-the-art generative diffusion models tailored to your project parameters.")
    
    rend_col1, rend_col2 = st.columns([1, 1], gap="medium")
    
    with rend_col1:
        arch_style = st.selectbox(
            "Architectural Visual Style",
            [
                "Modern Biophilic",
                "Contemporary Glass Facade",
                "Brutalist High-Tech",
                "Heritage Indo-Modern",
                "Industrial Logistics Hub"
            ],
            index=0
        )
        
        render_seed = st.number_input("Diffusion Seed", value=42, min_value=1, max_value=999999, step=1)
        
        render_url, generated_prompt = generate_architectural_render_url(
            structure_type=v_structure_type,
            grade=v_grade,
            location_tier=v_location_tier,
            custom_style=arch_style,
            seed=int(render_seed)
        )
        
        with st.expander("📝 Inspect Generative Architectural Prompt", expanded=False):
            st.code(generated_prompt, language="text")
            
        regenerate_render = st.button("🔄 Generate / Refresh 3D Conceptual Render", type="secondary", use_container_width=True)
        
    with rend_col2:
        st.image(
            render_url,
            caption=f"Conceptual 3D Visualization: {v_structure_type} ({arch_style})",
            use_container_width=True
        )
        st.markdown(f"[🔗 Open Full-Resolution 8K Render in Browser]({render_url})")


# =============================================================
# TAB 4: DAILY SITE ASSISTANT & WEATHER ADVISORY (EPIC 5)
# =============================================================
with tab4:
    st.markdown("### 🌦️ Daily Site Assistant & Weather-Aware Advisory (OSHA / IS 456)")
    st.caption("Real-time weather protocols for crane safety, concrete curing, and electrical hazards combined with an interactive multi-turn civil engineering assistant chatbot.")
    
    # Weather Protocol Section
    st.markdown("#### 1. Dynamic Site Weather Condition Selector")
    selected_weather = st.selectbox(
        "Current Environmental & Weather Condition",
        list(WEATHER_PROTOCOLS.keys()),
        index=0
    )
    
    proto = WEATHER_PROTOCOLS[selected_weather]
    
    # Weather Protocol Alert Cards
    w_col1, w_col2 = st.columns(2)
    
    with w_col1:
        st.markdown(f"""
        <div style="background: #1E293B; border-left: 5px solid {proto['status_color']}; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
            <div style="color: #F8FAFC; font-weight: 700; font-size: 1.05rem; margin-bottom: 4px;">
                🏗️ Crane & Tower Hoist Operations: {proto['crane_status']}
            </div>
            <div style="font-size: 0.88rem; color: #CBD5E1;">
                {proto['crane_detail']}
            </div>
        </div>
        
        <div style="background: #1E293B; border-left: 5px solid {proto['status_color']}; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
            <div style="color: #F8FAFC; font-weight: 700; font-size: 1.05rem; margin-bottom: 4px;">
                🧗 Scaffolding & Working at Heights: {proto['height_status']}
            </div>
            <div style="font-size: 0.88rem; color: #CBD5E1;">
                {proto['height_detail']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with w_col2:
        st.markdown(f"""
        <div style="background: #1E293B; border-left: 5px solid {proto['status_color']}; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
            <div style="color: #F8FAFC; font-weight: 700; font-size: 1.05rem; margin-bottom: 4px;">
                💧 Concrete Curing & Pouring Protocol: {proto['concrete_protocol']}
            </div>
            <div style="font-size: 0.88rem; color: #CBD5E1;">
                {proto['concrete_detail']}
            </div>
        </div>
        
        <div style="background: #1E293B; border-left: 5px solid {proto['status_color']}; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
            <div style="color: #F8FAFC; font-weight: 700; font-size: 1.05rem; margin-bottom: 4px;">
                ⚡ Electrical & Worker Welfare Protocols
            </div>
            <div style="font-size: 0.85rem; color: #CBD5E1;">
                <b>Electrical:</b> {proto['electrical_safety']}<br>
                <b>Welfare:</b> {proto['worker_welfare']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    
    # Interactive Construction Engineering Assistant Chatbot
    st.markdown("#### 2. Interactive Construction Engineering Assistant")
    st.caption("Ask questions regarding IS 456, OSHA guidelines, rebar detailing, concrete technology, striking periods, or safety protocols.")
    
    # Session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {
                "role": "assistant",
                "content": (
                    "Greetings. I am your **Chief Site Civil Engineer & OSHA / IS 456 Safety Director**. "
                    "How can I assist you with site inspection, concrete curing protocols, structural code compliance, or safety regulations today?"
                )
            }
        ]
        
    # Quick Preset Query Chips
    st.markdown("**⚡ Quick Inquiry Presets:**")
    preset_cols = st.columns(5)
    
    prompt_to_submit = None
    with preset_cols[0]:
        if st.button("M25 Curing Intervals in Summer", use_container_width=True):
            prompt_to_submit = "What are the curing intervals for M25 concrete in summer?"
    with preset_cols[1]:
        if st.button("OSHA Scaffolding Checklist", use_container_width=True):
            prompt_to_submit = "OSHA scaffolding inspection checklist"
    with preset_cols[2]:
        if st.button("IS 456 Permissible Crack Width", use_container_width=True):
            prompt_to_submit = "Permissible crack width under IS 456"
    with preset_cols[3]:
        if st.button("Steel Consumption per sq.ft", use_container_width=True):
            prompt_to_submit = "How to calculate steel consumption per sq.ft?"
    with preset_cols[4]:
        if st.button("Deep Trench Excavation Protocol", use_container_width=True):
            prompt_to_submit = "Safety protocol for deep trench excavation > 1.5 meters"

    # Render Chat History
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"], avatar="👷‍♂️" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])
            
    # Handle User Input
    chat_input = st.chat_input("Enter your structural engineering or site safety question here...")
    active_prompt = prompt_to_submit or chat_input
    
    if active_prompt:
        # Append User Message
        st.session_state["chat_history"].append({"role": "user", "content": active_prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(active_prompt)
            
        # Generate Response
        with st.chat_message("assistant", avatar="👷‍♂️"):
            with st.spinner("Consulting IS codes and OSHA structural standards..."):
                resp_text, is_live_chat = engine.generate_chat_response(
                    history=st.session_state["chat_history"][:-1],
                    user_message=active_prompt,
                    system_instruction=SITE_ENGINEER_CHAT_SYSTEM_PROMPT,
                    fallback_responder=get_fallback_engineering_response
                )
                st.markdown(resp_text)
                if not is_live_chat:
                    st.caption("ℹ️ *Response provided via Chief Engineer Knowledge Base (Demonstration Mode).*")
                    
        # Append Assistant Response
        st.session_state["chat_history"].append({"role": "assistant", "content": resp_text})

# -------------------------------------------------------------
# FOOTER
# -------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 10px 0;">
    Multimodal Construction Intelligence Platform &nbsp;|&nbsp; 
    Category: Generative AI & Real Estate Decision Support &nbsp;|&nbsp; 
    Platform ID: <code>6ac4c98d1dcde6d7857c1642</code> &nbsp;|&nbsp; 
    Engineered for Streamlit Cloud Deployment
</div>
""", unsafe_allow_html=True)
