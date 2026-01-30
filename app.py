import streamlit as st
import textwrap
from utils.ui import inject_global_css, page_header, glass_card, metric_card

st.set_page_config(
    page_title="HTS Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
)

inject_global_css()

# Hero Section
page_header(
    "Customs Intelligence Platform",
    "On-demand HTS alignment leveraging deep semantic architecture and industrial AI"
)

# Value Propositions
col1, col2, col3 = st.columns(3)
with col1:
    st.info("### Mitigate Risk\nEliminate customs penalties with precise, AI-validated classification logic.")
with col2:
    st.success("### Accelerate Entry\nReduce time-to-market with automated regulatory alignment and duty mapping.")
with col3:
    st.warning("### Scale Intelligence\nDeploy consistent trade compliance logic across global logistics networks.")

st.markdown("<br>", unsafe_allow_html=True)

# Main Intelligence Metrics
st.markdown('<h2 class="section-title">Global Trade Coverage</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("HTS Dataset", "2026 Active")
with col2:
    metric_card("Intelligence Depth", "35,571")
with col3:
    metric_card("Search Response", "<150ms")
with col4:
    metric_card("Global Reach", "100%")

st.markdown("<br>", unsafe_allow_html=True)

# Platform Intelligence Guide
st.markdown('<h2 class="section-title">Search & Classification Engine</h2>', unsafe_allow_html=True)

guide_content = textwrap.dedent("""
    #### 1. Professional Semantic Lookup
    Use **Customs Intelligence Search** for technical queries. 
    Our engine understands industrial terminology like "asynchronous motor" or "PET polymer".
    
    #### 2. Automated Classification Analysis
    Input full product specifications into the **Classification Assistant** 
    to receive instant HTS alignment with regulatory reasoning.
""").strip()

st.info(guide_content)

st.markdown("<br>", unsafe_allow_html=True)

# Intelligence Features
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Platform Capabilities")
    st.markdown("""
    - **AI-Powered:** OpenAI embeddings for semantic understanding
    - **Fast:** Sub-second response times for complex queries
    - **Accurate:** Advanced HTS code alignment logic
    - **Comprehensive:** Full 2026 HTS database coverage
    - **Explainable:** Detailed regulatory reasoning
    """)

with col2:
    st.markdown("### Best Practices")
    st.markdown("""
    - Start with natural product descriptions
    - Include material composition and final use
    - Specify industrial or retail packaging
    - Check confidence scores for compliance
    - Explore the HTS hierarchy for context
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #8b949e; font-size: 14px;">'
    'HTS Intelligence Platform &copy; 2026 | Built for Global Trade Professionals'
    '</div>',
    unsafe_allow_html=True
)
