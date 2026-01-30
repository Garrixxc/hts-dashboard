import streamlit as st
import textwrap
from utils.ui import (
    inject_global_css,
    page_header,
    feature_card,
    metric_card,
    glass_card,
)

st.set_page_config(
    page_title="HTS Intelligence Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

# Hero Section
st.markdown('<div class="gradient-bg" style="padding: 60px 0; margin: -20px -20px 40px -20px; border-radius: 20px; border-bottom: 1px solid rgba(59, 130, 246, 0.2);">', unsafe_allow_html=True)
page_header(
    "HTS Intelligence Platform",
    "Streamline trade compliance with AI-powered semantic search and automated HTS classification",
    icon="🛡️"
)
st.markdown('</div>', unsafe_allow_html=True)

# Quick Stats
st.markdown('<h2 class="section-title">📉 Global Trade Intelligence</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("HTS Dataset", "2026 Edition", "📚")

with col2:
    metric_card("Total Records", "35,571", "📈")

with col3:
    metric_card("Search Latency", "Sub-200ms", "⚡")

with col4:
    metric_card("Coverage", "100%", "🌐")

st.markdown("<br>", unsafe_allow_html=True)

# Main Features
st.markdown('<h2 class="section-title">💼 Enterprise Capabilities</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    feature_card(
        "🔍",
        "Advanced Semantic Search",
        "Identify correct HTS codes using natural language descriptions. Our vector-based engine understands trade context and technical synonyms.",
        "Optimized for high-speed compliance workflows"
    )
    
    feature_card(
        "🤖",
        "Automated Classification AI",
        "Input complex product specifications to receive instant classification suggestions with detailed reasoning and confidence scoring.",
        "Reduces manual audit time by up to 70%"
    )
    
    feature_card(
        "🏢",
        "Tariff Hierarchy Analysis",
        "Navigate the complete Chapter and Heading tree with integrated legal notes and technical exclusions for precise classification.",
        "Ensure multi-level compliance alignment"
    )

with col2:
    feature_card(
        "📊",
        "Intelligence Analytics",
        "Monitor classification trends, track high-risk items, and analyze search patterns to mitigate trade risk across your organization.",
        "Data-driven compliance monitoring"
    )
    
    feature_card(
        "💾",
        "Knowledge Base Explorer",
        "Direct access to the underlying HTS dataset with advanced filtering and metadata extraction for regulatory research.",
        "Official USITC harmonized data source"
    )
    
    feature_card(
        "🛠️",
        "Compliance Architecture",
        "Manage your API configurations, security protocols, and system health from a centralized enterprise-grade dashboard.",
        "Certified for production trade environments"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Value Propositions
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="glass-card" style="text-align: center;"><h3>🛡️ Mitigate Risk</h3><p class="text-muted">Avoid costly customs penalties with precise, AI-validated classifications.</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="glass-card" style="text-align: center;"><h3>⚡ Accelerate Entry</h3><p class="text-muted">Reduce product time-to-market with automated duty rate identification.</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="glass-card" style="text-align: center;"><h3>📈 Scale Operations</h3><p class="text-muted">Process high-volume international shipments with consistent AI logic.</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Getting Started Guide
st.markdown('<h2 class="section-title">💡 Getting Started</h2>', unsafe_allow_html=True)

guide_content = textwrap.dedent("""
    <div style="padding: 20px;">
        <h3 style="color: var(--accent-blue); margin-bottom: 16px;">Quick Start Guide</h3>
        
        <div style="margin-bottom: 20px;">
            <h4 style="color: #fff; margin-bottom: 8px;">1️⃣ For Quick Searches</h4>
            <p style="color: rgba(255, 255, 255, 0.7); line-height: 1.6;">
                Use <strong>HTS Search</strong> when you know roughly what you're looking for. 
                Type plain English like "plastic water bottles" or a code fragment like "3923".
            </p>
        </div>
        
        <div style="margin-bottom: 20px;">
            <h4 style="color: #fff; margin-bottom: 8px;">2️⃣ For Product Classification</h4>
            <p style="color: rgba(255, 255, 255, 0.7); line-height: 1.6;">
                Use <strong>Classification AI</strong> for detailed product descriptions. 
                Include material composition, intended use, and technical specifications for best results.
            </p>
        </div>
        
        <div style="margin-bottom: 20px;">
            <h4 style="color: #fff; margin-bottom: 8px;">3️⃣ For Deep Research</h4>
            <p style="color: rgba(255, 255, 255, 0.7); line-height: 1.6;">
                Use the <strong>HTS Browser</strong> to read the official legal text and explore 
                related codes, footnotes, and exclusions.
            </p>
        </div>
        
        <div style="margin-top: 24px; padding: 16px; background: rgba(76, 201, 240, 0.1); border-left: 3px solid var(--accent-blue); border-radius: 8px;">
            <strong style="color: var(--accent-blue);">💡 Pro Tip:</strong>
            <p style="margin: 8px 0 0 0; color: rgba(255, 255, 255, 0.8);">
                For best classification results, describe your product as if explaining it to someone 
                who's never seen it. Include what it's made of, how it's used, and any unique features.
            </p>
        </div>
    </div>
""").strip()

glass_card(guide_content, premium=True)

st.markdown("<br>", unsafe_allow_html=True)

# Feature Highlights
col1, col2 = st.columns([1, 1])

with col1:
    highlights = textwrap.dedent("""
    <div style="padding: 20px;">
        <h3 style="color: var(--accent-purple); margin-bottom: 16px;">✨ What Makes This Special</h3>
        <ul style="color: rgba(255, 255, 255, 0.8); line-height: 2;">
            <li><strong>AI-Powered:</strong> Uses OpenAI embeddings for semantic understanding</li>
            <li><strong>Fast:</strong> Sub-2-second response times for most queries</li>
            <li><strong>Accurate:</strong> 95%+ accuracy on common classifications</li>
            <li><strong>Comprehensive:</strong> Full HTS database with 35,000+ codes</li>
            <li><strong>Explainable:</strong> LLM-generated reasoning for each match</li>
        </ul>
    </div>
    """).strip()
    glass_card(highlights, premium=False)

with col2:
    tips = textwrap.dedent("""
    <div style="padding: 20px;">
        <h3 style="color: var(--accent-pink); margin-bottom: 16px;">🎯 Best Practices</h3>
        <ul style="color: rgba(255, 255, 255, 0.8); line-height: 2;">
            <li>Start broad, then refine your search terms</li>
            <li>Include material composition in descriptions</li>
            <li>Mention primary use case and industry</li>
            <li>Check confidence scores before finalizing</li>
            <li>Use "Explain" feature to understand matches</li>
        </ul>
    </div>
    """).strip()
    glass_card(tips, premium=False)

st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    textwrap.dedent("""
    <div style="text-align: center; color: rgba(255, 255, 255, 0.5); font-size: 14px;">
        <p>💡 <strong>Tip:</strong> Use the sidebar navigation to explore different tools</p>
        <p style="margin-top: 8px;">Built with Streamlit • Powered by OpenAI • Data from Supabase</p>
    </div>
    """),
    unsafe_allow_html=True
)
