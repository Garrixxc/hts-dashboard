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
st.markdown('<div class="gradient-bg" style="padding: 60px 0; margin: -20px -20px 40px -20px; border-radius: 20px; border-bottom: 2px solid var(--accent-primary);">', unsafe_allow_html=True)
page_header(
    "Customs Intelligence Platform",
    "On-demand HTS alignment leveraging deep semantic architecture and industrial AI",
    icon="🛡️"
)
st.markdown('</div>', unsafe_allow_html=True)

# Value Propositions
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="glass-card" style="text-align: center; border-top: 4px solid var(--accent-primary);"><h3>🛡️ Mitigate Risk</h3><p style="color: var(--text-muted); font-size: 14px;">Eliminate customs penalties with precise, AI-validated classification logic.</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="glass-card" style="text-align: center; border-top: 4px solid var(--accent-secondary);"><h3>⚡ Accelerate Entry</h3><p style="color: var(--text-muted); font-size: 14px;">Reduce time-to-market with automated regulatory alignment and duty mapping.</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="glass-card" style="text-align: center; border-top: 4px solid var(--accent-vibrant);"><h3>📈 Scale Intelligence</h3><p style="color: var(--text-muted); font-size: 14px;">Deploy consistent trade compliance logic across global logistics networks.</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Intelligence Metrics
st.markdown('<h2 class="section-title">📊 Global Trade Coverage</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("HTS Dataset", "2026 Active", "📚")
with col2:
    metric_card("Intelligence Depth", "35,571", "📈")
with col3:
    metric_card("Search Response", "<150ms", "⚡")
with col4:
    metric_card("Global Reach", "100%", "🌐")

st.markdown("<br>", unsafe_allow_html=True)

# Platform Intelligence Guide
st.markdown('<h2 class="section-title">🚀 Search & Classification Engine</h2>', unsafe_allow_html=True)

guide_content = textwrap.dedent("""
    <div style="padding: 12px;">
        <div style="margin-bottom: 24px;">
            <h4 style="color: var(--accent-primary); margin-bottom: 8px;">1. Professional Semantic Lookup</h4>
            <p style="color: var(--text-muted); line-height: 1.6;">
                Use <strong>Customs Intelligence Search</strong> for technical queries. 
                Our engine understands industrial terminology like "asynchronous motor" or "PET polymer".
            </p>
        </div>
        
        <div style="margin-bottom: 24px;">
            <h4 style="color: var(--accent-primary); margin-bottom: 8px;">2. Automated Classification Analysis</h4>
            <p style="color: var(--text-muted); line-height: 1.6;">
                Input full product specifications into the <strong>Classification Assistant</strong> 
                to receive instant HTS alignment with regulatory reasoning.
            </p>
        </div>
        
        <div style="margin-top: 24px; padding: 16px; background: rgba(79, 70, 229, 0.05); border-left: 4px solid var(--accent-primary); border-radius: 8px;">
            <strong style="color: var(--accent-primary);">💡 Intelligence Tip:</strong>
            <p style="margin: 8px 0 0 0; color: var(--text-main);">
                For optimal results, provide material composition and intended industrial application. 
                The AI scales best when given high-resolution technical data.
            </p>
        </div>
    </div>
""").strip()

glass_card(guide_content, premium=True)

st.markdown("<br>", unsafe_allow_html=True)

# Intelligence Features
col1, col2 = st.columns([1, 1])

with col1:
    features = textwrap.dedent("""
    <div style="padding: 20px;">
        <h3 style="color: var(--accent-primary); margin-bottom: 16px;">✨ Platform Capabilities</h3>
        <ul style="color: var(--text-muted); line-height: 2;">
            <li><strong>AI-Powered:</strong> OpenAI embeddings for semantic understanding</li>
            <li><strong>Fast:</strong> Sub-second response times for complex queries</li>
            <li><strong>Accurate:</strong> Advanced HTS code alignment logic</li>
            <li><strong>Comprehensive:</strong> Full 2026 HTS database coverage</li>
            <li><strong>Explainable:</strong> Detailed regulatory reasoning for each match</li>
        </ul>
    </div>
    """).strip()
    glass_card(features, premium=False)

with col2:
    best_practices = textwrap.dedent("""
    <div style="padding: 20px;">
        <h3 style="color: var(--accent-secondary); margin-bottom: 16px;">🎯 Best Practices</h3>
        <ul style="color: var(--text-muted); line-height: 2;">
            <li>Start with natural product descriptions</li>
            <li>Include material composition and final use</li>
            <li>Specify industrial or retail packaging</li>
            <li>Check confidence scores for compliance audits</li>
            <li>Explore the HTS hierarchy for legal context</li>
        </ul>
    </div>
    """).strip()
    glass_card(best_practices, premium=False)

st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.markdown(
    '<div style="text-align: center; padding: 40px; color: var(--text-muted); font-size: 14px;">'
    'HTS Intelligence Platform &copy; 2026 | Built for Global Trade Professionals'
    '</div>',
    unsafe_allow_html=True
)
