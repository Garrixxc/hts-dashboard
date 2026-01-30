import streamlit as st
import textwrap
from utils.ui import inject_global_css, page_header, glass_card

st.set_page_config(
    page_title="Analytics - HTS Dashboard",
    page_icon="📊",
    layout="wide",
)

inject_global_css()

page_header(
    "Analytics Dashboard",
    "Track your search history, most-used codes, and classification patterns over time",
    icon="📊"
)

st.markdown('<h3 class="section-title" style="font-size: 20px; margin-top: 24px;">📈 Enterprise Intelligence Overview</h3>', unsafe_allow_html=True)

# Mock Data for professional lookup
col1, col2, col3 = st.columns(3)
with col1:
    metric_card("Monthly Classifications", "1,284", "📅")
with col2:
    metric_card("Accuracy Rate", "99.2%", "🎯")
with col3:
    metric_card("Compliance Risk Score", "Low", "🛡️")

st.markdown("<br>", unsafe_allow_html=True)

# Main Intelligence Card
content = textwrap.dedent("""
    <div style="padding: 24px;">
        <h3 style="color: var(--accent-blue); margin-bottom: 16px; font-weight: 700;">Classification Velocity</h3>
        <p style="font-size: 14px; line-height: 1.6; color: var(--accent-slate); margin-bottom: 24px;">
            Real-time monitoring of HTS alignment efficiency across global trade lanes.
        </p>
        
        <div style="display: flex; gap: 8px; align-items: flex-end; height: 120px; margin-bottom: 20px;">
            <div style="flex: 1; background: var(--accent-blue); height: 40%; border-radius: 4px 4px 0 0; opacity: 0.6;"></div>
            <div style="flex: 1; background: var(--accent-blue); height: 65%; border-radius: 4px 4px 0 0; opacity: 0.7;"></div>
            <div style="flex: 1; background: var(--accent-blue); height: 85%; border-radius: 4px 4px 0 0; opacity: 0.8;"></div>
            <div style="flex: 1; background: var(--accent-blue); height: 55%; border-radius: 4px 4px 0 0; opacity: 0.6;"></div>
            <div style="flex: 1; background: var(--accent-blue); height: 95%; border-radius: 4px 4px 0 0; opacity: 0.9;"></div>
            <div style="flex: 1; background: var(--accent-blue); height: 75%; border-radius: 4px 4px 0 0; opacity: 0.8;"></div>
            <div style="flex: 1; background: var(--accent-blue); height: 80%; border-radius: 4px 4px 0 0; opacity: 0.8;"></div>
        </div>
        
        <div style="display: flex; justify-content: space-between; font-size: 11px; color: var(--accent-slate);">
            <span>MON</span><span>TUE</span><span>WED</span><span>THU</span><span>FRI</span><span>SAT</span><span>SUN</span>
        </div>
    </div>
""").strip()

glass_card(content, premium=True)

st.markdown("<br>", unsafe_allow_html=True)

# Industry Distribution
st.markdown('<h3 class="section-title" style="font-size: 20px;">🌐 Chapter Distribution</h3>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    distribution = textwrap.dedent("""
        <div style="padding: 20px;">
            <h4 style="color: #fff; margin-bottom: 16px; font-size: 16px;">Top Chapters by Volume</h4>
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px;">
                    <span>Chapter 84: Machinery & Parts</span><span>42%</span>
                </div>
                <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.05); border-radius: 10px;">
                    <div style="width: 42%; height: 100%; background: var(--accent-blue); border-radius: 10px;"></div>
                </div>
            </div>
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px;">
                    <span>Chapter 85: Electrical Equipment</span><span>28%</span>
                </div>
                <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.05); border-radius: 10px;">
                    <div style="width: 28%; height: 100%; background: var(--accent-blue); border-radius: 10px;"></div>
                </div>
            </div>
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px;">
                    <span>Chapter 39: Plastics</span><span>15%</span>
                </div>
                <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.05); border-radius: 10px;">
                    <div style="width: 15%; height: 100%; background: var(--accent-blue); border-radius: 10px;"></div>
                </div>
            </div>
        </div>
    """).strip()
    glass_card(distribution, premium=False)

with col_b:
    summary = textwrap.dedent("""
        <div style="padding: 20px;">
            <h4 style="color: #fff; margin-bottom: 16px; font-size: 16px;">Compliance Stability</h4>
            <p style="font-size: 14px; color: var(--accent-slate); line-height: 1.6;">
                System maintains high alignment stability across core industrial categories. No significant drift detected in last 30 business cycles.
            </p>
            <div style="margin-top: 16px; padding: 12px; background: rgba(16, 185, 129, 0.05); border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.2);">
                <span style="color: var(--success); font-weight: 600; font-size: 13px;">✓ System Status: Optimal</span>
            </div>
        </div>
    """).strip()
    glass_card(summary, premium=False)

glass_card(viz_content, premium=False)

# Sidebar
with st.sidebar:
    st.markdown("### 💡 Analytics Tips")
    
    tips = textwrap.dedent("""
    <div class="glass-card">
        <p style="font-size: 14px; line-height: 1.6; color: rgba(255, 255, 255, 0.8);">
            <strong>To implement analytics:</strong>
        </p>
        <ol style="font-size: 13px; line-height: 1.8; color: rgba(255, 255, 255, 0.7); margin-top: 12px;">
            <li>Create a Supabase table for logs</li>
            <li>Add logging to search functions</li>
            <li>Use Plotly for visualizations</li>
            <li>Set up scheduled aggregations</li>
        </ol>
    </div>
    """).strip()
    st.markdown(tips, unsafe_allow_html=True)
