import streamlit as st
import textwrap
from utils.ui import inject_global_css, page_header, glass_card, metric_card

st.set_page_config(
    page_title="Analytics - HTS Dashboard",
    page_icon="📊",
    layout="wide",
)

inject_global_css()

page_header(
    "Enterprise Intelligence Overview",
    "Monitor classification velocity, accuracy trends, and regulatory risk across the organization.",
    icon="📊"
)

# Top Metrics
st.markdown('<h2 class="section-title">📈 System-Wide Performance</h2>', unsafe_allow_html=True)
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

with m_col1:
    metric_card("Monthly Classifications", "1,284", "📅")

with m_col2:
    metric_card("Average Accuracy", "98.2%", "🎯")

with m_col3:
    metric_card("Compliance Risk", "Minimal", "🛡️")

with m_col4:
    metric_card("Processing Speed", "142ms", "⚡")

st.markdown("<br>", unsafe_allow_html=True)

# Main Analytics Section
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<h3 class="section-title" style="font-size: 20px;">📉 Classification Velocity</h3>', unsafe_allow_html=True)
    
    # Custom chart visualization using CSS
    chart_content = textwrap.dedent("""
        <div style="height: 300px; display: flex; align-items: flex-end; gap: 10px; padding: 20px; background: #f1f5f9; border-radius: 12px; border: 1px solid var(--border-subtle);">
            <div style="flex: 1; height: 40%; background: linear-gradient(to top, var(--accent-primary), var(--accent-vibrant)); border-radius: 4px 4px 0 0;" title="Jan"></div>
            <div style="flex: 1; height: 55%; background: linear-gradient(to top, var(--accent-primary), var(--accent-vibrant)); border-radius: 4px 4px 0 0;" title="Feb"></div>
            <div style="flex: 1; height: 48%; background: linear-gradient(to top, var(--accent-primary), var(--accent-vibrant)); border-radius: 4px 4px 0 0;" title="Mar"></div>
            <div style="flex: 1; height: 70%; background: linear-gradient(to top, var(--accent-primary), var(--accent-vibrant)); border-radius: 4px 4px 0 0;" title="Apr"></div>
            <div style="flex: 1; height: 85%; background: linear-gradient(to top, var(--accent-primary), var(--accent-vibrant)); border-radius: 4px 4px 0 0;" title="May"></div>
            <div style="flex: 1; height: 75%; background: linear-gradient(to top, var(--accent-primary), var(--accent-vibrant)); border-radius: 4px 4px 0 0;" title="Jun"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 10px; color: var(--text-muted); font-size: 11px; padding: 0 10px;">
            <span>Jan</span><span>Feb</span><span>Mar</span><span>Apr</span><span>May</span><span>Jun</span>
        </div>
    """).strip()
    glass_card(chart_content, premium=True)

with col_right:
    st.markdown('<h3 class="section-title" style="font-size: 20px;">🛡️ Risk Profile</h3>', unsafe_allow_html=True)
    
    risk_content = textwrap.dedent("""
        <div style="padding: 24px; text-align: center;">
            <div style="font-size: 48px; margin-bottom: 20px;">✅</div>
            <h4 style="color: var(--text-main); margin-bottom: 8px;">Compliance Status: Low</h4>
            <p style="color: var(--text-muted); font-size: 14px; line-height: 1.6;">
                99.4% of classifications align with USITC benchmarks. No anomalies detected.
            </p>
        </div>
    """).strip()
    glass_card(risk_content, premium=False)

st.markdown("<br>", unsafe_allow_html=True)

# Industry Distribution
st.markdown('<h3 class="section-title" style="font-size: 20px;">🌐 Chapter Distribution</h3>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    distribution = textwrap.dedent("""
        <div style="padding: 20px;">
            <h4 style="color: var(--text-main); margin-bottom: 16px; font-size: 16px;">Top Chapters by Volume</h4>
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px; color: var(--text-muted);">
                    <span>Chapter 84: Machinery & Parts</span><span>42%</span>
                </div>
                <div style="width: 100%; height: 6px; background: #e2e8f0; border-radius: 10px;">
                    <div style="width: 42%; height: 100%; background: var(--accent-primary); border-radius: 10px;"></div>
                </div>
            </div>
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px; color: var(--text-muted);">
                    <span>Chapter 85: Electrical Equipment</span><span>28%</span>
                </div>
                <div style="width: 100%; height: 6px; background: #e2e8f0; border-radius: 10px;">
                    <div style="width: 28%; height: 100%; background: var(--accent-primary); border-radius: 10px;"></div>
                </div>
            </div>
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px; color: var(--text-main);">
                    <span>Chapter 39: Plastics</span><span>15%</span>
                </div>
                <div style="width: 100%; height: 6px; background: #e2e8f0; border-radius: 10px;">
                    <div style="width: 15%; height: 100%; background: var(--accent-primary); border-radius: 10px;"></div>
                </div>
            </div>
        </div>
    """).strip()
    glass_card(distribution, premium=False)

with col_b:
    summary = textwrap.dedent("""
        <div style="padding: 20px;">
            <h4 style="color: var(--text-main); margin-bottom: 16px; font-size: 16px;">Compliance Stability</h4>
            <p style="font-size: 14px; color: var(--text-muted); line-height: 1.6;">
                System maintains high alignment stability across core industrial categories. No significant drift detected in last 30 business cycles.
            </p>
            <div style="margin-top: 16px; padding: 12px; background: rgba(16, 185, 129, 0.05); border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.2);">
                <span style="color: var(--vibrant-green); font-weight: 600; font-size: 13px;">✓ Analysis Status: Optimal</span>
            </div>
        </div>
    """).strip()
    glass_card(summary, premium=False)

viz_content = textwrap.dedent("""
<div style="padding: 20px; text-align: center;">
    <p style="font-size: 14px; color: var(--text-muted);">
        Predictive classification trends for upcoming fiscal cycles.
    </p>
    <br>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 20px;">
        <div style="padding: 16px; background: rgba(88, 166, 255, 0.05); border-radius: 12px; border: 1px solid var(--border-subtle);">
            <div style="font-size: 32px; color: var(--primary);">📊</div>
            <p style="margin-top: 8px; font-size: 13px; color: var(--text-main);">Trends</p>
        </div>
        <div style="padding: 16px; background: rgba(88, 166, 255, 0.05); border-radius: 12px; border: 1px solid var(--border-subtle);">
            <div style="font-size: 32px; color: var(--secondary);">🎯</div>
            <p style="margin-top: 8px; font-size: 13px; color: var(--text-main);">Accuracy</p>
        </div>
        <div style="padding: 16px; background: rgba(88, 166, 255, 0.05); border-radius: 12px; border: 1px solid var(--border-subtle);">
            <div style="font-size: 32px; color: #bc8cff;">🧠</div>
            <p style="margin-top: 8px; font-size: 13px; color: var(--text-main);">AI Flow</p>
        </div>
    </div>
</div>
""").strip()

glass_card(viz_content, premium=False)

# Sidebar
with st.sidebar:
    st.markdown("### 💡 Analytics Tips")
    
    tips = textwrap.dedent("""
    <div class="glass-card">
        <p style="font-size: 14px; line-height: 1.6; color: var(--text-main);">
            <strong>To implement live analytics:</strong>
        </p>
        <ol style="font-size: 13px; line-height: 1.8; color: var(--text-muted); margin-top: 12px;">
            <li>Create a Supabase table for logs</li>
            <li>Add logging to search functions</li>
            <li>Use <code>st.cache_data</code> for speed</li>
            <li>Aggregate by HTS Chapter</li>
        </ol>
    </div>
    """).strip()
    st.markdown(tips, unsafe_allow_html=True)
