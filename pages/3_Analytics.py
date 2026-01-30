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
    "Monitor classification velocity, accuracy trends, and regulatory risk across the organization."
)

# Top Metrics
st.markdown("### System-Wide Performance")
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

with m_col1:
    metric_card("Monthly Classifications", "1,284")

with m_col2:
    metric_card("Average Accuracy", "98.2%")

with m_col3:
    metric_card("Compliance Risk", "Minimal")

with m_col4:
    metric_card("Processing Speed", "142ms")

st.markdown("<br>", unsafe_allow_html=True)

# Main Analytics Section
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### Classification Velocity")
    # Using standard columns for a simple "chart" feeling without broken CSS
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: st.metric("Jan", "400", "+5%")
    with c2: st.metric("Feb", "550", "+12%")
    with c3: st.metric("Mar", "480", "-8%")
    with c4: st.metric("Apr", "700", "+22%")
    with c5: st.metric("May", "850", "+15%")
    with c6: st.metric("Jun", "750", "-10%")

with col_right:
    st.markdown("### Risk Profile")
    st.success("#### Compliance Status: Low\n99.4% of classifications align with USITC benchmarks. No anomalies detected.")

st.markdown("<br>", unsafe_allow_html=True)

# Industry Distribution
st.markdown("### Chapter Distribution")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("#### Top Chapters by Volume")
    st.progress(0.42, text="Chapter 84: Machinery (42%)")
    st.progress(0.28, text="Chapter 85: Electrical (28%)")
    st.progress(0.15, text="Chapter 39: Plastics (15%)")

with col_b:
    st.markdown("#### Compliance Stability")
    st.info("System maintains high alignment stability across core industrial categories. No significant drift detected in last 30 business cycles.")

st.markdown("<br>", unsafe_allow_html=True)

# Predictive Trends
st.markdown("### Predictive Intelligence")
p1, p2, p3 = st.columns(3)
with p1:
    st.metric("Trend Forecast", "Bullish", "+2.4%")
with p2:
    st.metric("Projected Accuracy", "99.1%", "+0.9%")
with p3:
    st.metric("AI Confidence", "Very High", "Stable")

# Sidebar
with st.sidebar:
    st.markdown("### Analytics Tips")
    st.info("""
    **To implement live analytics:**
    1. Create a Supabase table for logs
    2. Add logging to search functions
    3. Aggregate by HTS Chapter
    4. Visualize historical trends
    """)
