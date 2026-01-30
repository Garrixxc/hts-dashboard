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

st.markdown('<h3 class="section-title" style="font-size: 20px; margin-top: 24px;">📈 Usage Overview</h3>', unsafe_allow_html=True)

# Placeholder for future analytics
content = textwrap.dedent("""
    <div style="padding: 20px; text-align: center;">
        <div style="font-size: 48px; margin-bottom: 16px;">📊</div>
        <h3 style="color: var(--accent-blue); margin-bottom: 12px;">Analytics Coming Soon</h3>
        <p style="font-size: 14px; line-height: 1.6; color: rgba(255, 255, 255, 0.7);">
            You haven't wired up analytics logging to Supabase yet, so there's nothing to chart here.
        </p>
        <br>
        <p style="font-size: 14px; line-height: 1.6; color: rgba(255, 255, 255, 0.6);">
            When you're ready, store each search in a <code>search_logs</code> table and surface 
            those metrics here (e.g., most common queries, error rate, etc.).
        </p>
    </div>
""").strip()

glass_card(content, premium=True)

st.markdown("<br>", unsafe_allow_html=True)

# Future features
col1, col2 = st.columns(2)

with col1:
    features = textwrap.dedent("""
    <div style="padding: 20px;">
        <h4 style="color: var(--accent-purple); margin-bottom: 16px;">📊 Planned Metrics</h4>
        <ul style="font-size: 14px; line-height: 2; color: rgba(255, 255, 255, 0.8);">
            <li>Search count per day</li>
            <li>Top queries and keywords</li>
            <li>Zero-result queries</li>
            <li>Chapter distribution</li>
            <li>Classification accuracy</li>
            <li>Average confidence scores</li>
        </ul>
    </div>
    """).strip()
    glass_card(features, premium=False)

with col2:
    implementation = textwrap.dedent("""
    <div style="padding: 20px;">
        <h4 style="color: var(--accent-pink); margin-bottom: 16px;">🔧 Implementation Ideas</h4>
        <ul style="font-size: 14px; line-height: 2; color: rgba(255, 255, 255, 0.8);">
            <li>Create <code>search_logs</code> table</li>
            <li>Log each search with timestamp</li>
            <li>Track user sessions</li>
            <li>Store confidence scores</li>
            <li>Monitor error rates</li>
            <li>Generate weekly reports</li>
        </ul>
    </div>
    """).strip()
    glass_card(implementation, premium=False)

st.markdown("<br>", unsafe_allow_html=True)

# Sample visualization placeholder
st.markdown('<h3 class="section-title" style="font-size: 20px;">📈 Sample Visualizations</h3>', unsafe_allow_html=True)

viz_content = textwrap.dedent("""
<div style="padding: 20px; text-align: center;">
    <p style="font-size: 14px; color: rgba(255, 255, 255, 0.7);">
        Once analytics are implemented, you'll see charts here showing:
    </p>
    <br>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 20px;">
        <div style="padding: 16px; background: rgba(76, 201, 240, 0.1); border-radius: 12px;">
            <div style="font-size: 32px; color: var(--accent-blue);">📊</div>
            <p style="margin-top: 8px; font-size: 13px;">Search Trends</p>
        </div>
        <div style="padding: 16px; background: rgba(114, 9, 183, 0.1); border-radius: 12px;">
            <div style="font-size: 32px; color: var(--accent-purple);">🎯</div>
            <p style="margin-top: 8px; font-size: 13px;">Top Codes</p>
        </div>
        <div style="padding: 16px; background: rgba(247, 37, 133, 0.1); border-radius: 12px;">
            <div style="font-size: 32px; color: var(--accent-pink);">⚡</div>
            <p style="margin-top: 8px; font-size: 13px;">Performance</p>
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
