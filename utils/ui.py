"""
HTS Dashboard - Standard UI Components Library

This module provides clean, professional UI components that align with 
standard Streamlit behavior while adding polished refinements.
"""

import streamlit as st
import textwrap


def inject_global_css() -> None:
    """Inject clean, professional CSS that doesn't break standard components."""
    st.markdown(
        textwrap.dedent("""
        <style>
            /* Clean Typography */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
            
            :root {
                --primary-color: #58a6ff;
                --text-main: #f0f6fc;
                --text-muted: #8b949e;
            }
            
            /* Enhanced Card Styling */
            .glass-card {
                background: rgba(22, 27, 34, 0.6);
                border: 1px solid rgba(48, 54, 61, 0.8);
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
            }
            
            .glass-card-premium {
                background: rgba(22, 27, 34, 0.8);
                border: 1px solid rgba(88, 166, 255, 0.3);
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 20px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            }
            
            /* Professional Section Titles */
            .section-title {
                font-family: 'Inter', sans-serif;
                font-size: 20px;
                font-weight: 700;
                color: #f0f6fc;
                margin: 24px 0 16px 0;
                border-left: 4px solid var(--primary-color);
                padding-left: 12px;
            }
            
            /* Responsive adjustments */
            @media (max-width: 768px) {
                .glass-card { padding: 15px; }
            }
            
            /* Fix for overlapping text in some components */
            .stMarkdown p {
                line-height: 1.6;
            }
        </style>
        """),
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str | None = None, icon: str = "") -> None:
    """Render a clean page header."""
    header_html = f"## {icon} {title}" if icon else f"## {title}"
    st.markdown(header_html)
    if subtitle:
        st.markdown(f"*{subtitle}*")
    st.markdown("---")


def glass_card(content: str, premium: bool = False) -> None:
    """Render a card with professional styling."""
    card_class = "glass-card-premium" if premium else "glass-card"
    st.markdown(
        f'<div class="{card_class}">{content}</div>',
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str) -> None:
    """Render a clean metric card."""
    content = textwrap.dedent(f"""
        <div style="text-align: left;">
            <div style="font-size: 12px; color: #8b949e; text-transform: uppercase; font-weight: 600;">{label}</div>
            <div style="font-size: 24px; font-weight: 700; color: #f0f6fc;">{value}</div>
        </div>
    """).strip()
    glass_card(content)


def confidence_badge(score: float) -> str:
    """Generate a simple confidence indicator."""
    percentage = int(score * 100)
    color = "#3fb950" if score > 0.8 else "#f0883e" if score > 0.6 else "#f85149"
    return f'<span style="color: {color}; font-weight: 700;">{percentage}% Confidence</span>'


def similarity_bar(score: float) -> str:
    """Generate a simple similarity bar."""
    percentage = int(score * 100)
    return textwrap.dedent(f"""
        <div style="width: 100%; height: 4px; background: #30363d; border-radius: 2px; margin: 8px 0;">
            <div style="width: {percentage}%; height: 100%; background: #58a6ff; border-radius: 2px;"></div>
        </div>
    """).strip()


def result_card(
    hts_code: str,
    title: str,
    description: str,
    similarity: float = 0.0,
    duty_rate: str = "",
    show_explain: bool = False,
) -> None:
    """Render a clean result card."""
    confidence = confidence_badge(similarity) if similarity > 0 else ""
    sim_bar = similarity_bar(similarity) if similarity > 0 else ""
    
    content = textwrap.dedent(f"""
        <div style="margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h3 style="margin: 0; color: #58a6ff;">{hts_code}</h3>
                    <div style="font-weight: 600; font-size: 16px; margin-top: 4px;">{title}</div>
                </div>
                {confidence}
            </div>
            {sim_bar}
            <div style="font-size: 14px; color: #8b949e; margin-top: 8px;">
                {description}
            </div>
        </div>
    """).strip()
    
    glass_card(content)


def duty_tag(rate: str) -> str:
    """Legacy helper for duty tags."""
    return f'<span style="padding: 2px 8px; border-radius: 4px; font-size: 12px; background: rgba(88, 166, 255, 0.1); color: #58a6ff;">{rate}</span>'
