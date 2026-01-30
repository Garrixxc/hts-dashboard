"""
HTS Dashboard - Enhanced UI Components Library

This module provides a comprehensive design system with glassmorphism effects,
modern components, and utilities for building a premium dashboard experience.
"""

import streamlit as st
import textwrap


def inject_global_css() -> None:
    """Inject enhanced global CSS with glassmorphism and modern design."""
    st.markdown(
        textwrap.dedent("""
        <style>
            /* ============================================================================ */
            /* CSS VARIABLES - Design Tokens */
            /* ============================================================================ */
            :root {
                /* Primary Theme Colors - Hyper Vibrant */
                --primary: #6366f1;          /* Indigo-500 */
                --primary-vibrant: #4f46e5;  /* Indigo-600 */
                --secondary: #f59e0b;        /* Amber-500 */
                --vibrant-green: #10b981;    /* Emerald-500 */
                --vibrant-rose: #f43f5e;     /* Rose-500 */
                
                /* Layout Backgrounds */
                --bg-main: #ffffff;
                --bg-sidebar: #f8fafc;       /* Slate-50 */
                --bg-card: #ffffff;
                --bg-secondary: #f1f5f9;     /* Slate-100 */
                
                /* Typography */
                --text-main: #1e293b;        /* Slate-800 */
                --text-muted: #64748b;       /* Slate-500 */
                --text-on-vibrant: #ffffff;
                
                /* Borders & Shadows */
                --border-light: #e2e8f0;
                --shadow-vibrant: 0 10px 15px -3px rgba(99, 102, 241, 0.1);

                /* LEGACY ALIASES - Support for old variable names */
                --accent-primary: var(--primary);
                --accent-secondary: var(--secondary);
                --accent-vibrant: var(--vibrant-green);
                --accent-blue: var(--primary);
                --accent-purple: var(--primary-vibrant);
                --accent-amber: var(--secondary);
                --accent-orange: #f97316;    /* Orange-500 */
                --accent-gold: #f59e0b;
                --accent-stone: var(--text-muted);
                
                --success: var(--vibrant-green);
                --warning: var(--secondary);
                --error: var(--vibrant-rose);
                --info: #0ea5e9;             /* Sky-500 */
                
                --bg-dark: var(--bg-main);
                --bg-card: white;
                --bg-glass: rgba(255, 255, 255, 0.9);
                --bg-glass-hover: #f1f5f9;
                
                --border-subtle: var(--border-light);
                --border-medium: #cbd5e1;
                
                --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                --shadow-premium: var(--shadow-vibrant);
                
                --font-heading: 'Inter', sans-serif;
                --font-body: 'Inter', sans-serif;
            }
            
            /* High-Level Streamlit Theme Injection */
            [data-testid="stAppViewContainer"] {
                background-color: var(--bg-main) !important;
                color: var(--text-main) !important;
            }
            
            [data-testid="stSidebar"] {
                background-color: var(--bg-sidebar) !important;
                border-right: 1px solid var(--border-light) !important;
            }

            [data-testid="stHeader"] {
                background-color: rgba(255, 255, 255, 0.8) !important;
                backdrop-filter: blur(10px);
            }

            /* Fix Sidebar Text & Icons */
            [data-testid="stSidebar"] * {
                color: var(--text-main) !important;
            }

            /* Global Typography Fixes */
            h1, h2, h3, h4, h5, h6, p, li, label, .stMarkdown {
                color: var(--text-main) !important;
                font-family: 'Inter', sans-serif !important;
            }

            /* ============================================================================ */
            /* WIDGET STYLING - FIXING READABILITY */
            /* ============================================================================ */
            
            /* Standard Buttons */
            .stButton > button {
                background: var(--bg-secondary) !important;
                color: var(--text-main) !important;
                border: 1px solid var(--border-light) !important;
                border-radius: 8px !important;
                font-weight: 500 !important;
                transition: all 0.2s ease !important;
            }
            
            .stButton > button:hover {
                border-color: var(--primary) !important;
                color: var(--primary) !important;
                transform: translateY(-1px);
                box-shadow: var(--shadow-vibrant);
            }

            /* Primary/Action Buttons */
            div[data-testid="stFormSubmitButton"] button, 
            .btn-primary {
                background: linear-gradient(135deg, var(--primary), var(--primary-vibrant)) !important;
                color: white !important;
                border: none !important;
                box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.4) !important;
            }
            
            /* Text Inputs & Areas */
            .stTextInput input, .stTextArea textarea {
                background-color: var(--bg-secondary) !important;
                color: var(--text-main) !important;
                border: 1px solid var(--border-light) !important;
                border-radius: 8px !important;
            }

            .stTextInput input:focus, .stTextArea textarea:focus {
                border-color: var(--primary) !important;
                box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
            }

            /* ============================================================================ */
            /* GLASSMORPHISM COMPONENTS */
            /* ============================================================================ */
            
            .glass-card {
                background: white;
                border: 1px solid var(--border-light);
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                transition: all 0.3s ease;
            }
            
            .glass-card:hover {
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
                border-color: var(--primary);
                transform: translateY(-2px);
            }
            
            .glass-card-premium {
                background: white;
                border: 1px solid var(--border-light);
                border-radius: 16px;
                padding: 28px;
                margin-bottom: 24px;
                box-shadow: 0 20px 25px -5px rgba(99, 102, 241, 0.1);
                border-top: 4px solid var(--primary);
            }
            
            /* Section Headers with Vibrant Underline */
            .section-title {
                font-size: 24px;
                font-weight: 800;
                color: var(--text-main);
                margin-bottom: 20px;
                position: relative;
                padding-bottom: 8px;
            }
            
            .section-title::after {
                content: "";
                position: absolute;
                bottom: 0;
                left: 0;
                width: 40px;
                height: 4px;
                background: var(--primary);
                border-radius: 2px;
            }
            
            /* ============================================================================ */
            /* BADGES & TAGS */
            /* ============================================================================ */
            
            .badge {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 6px 12px;
                border-radius: 999px;
                font-size: 13px;
                font-weight: 600;
                transition: all 0.2s ease;
            }
            
            .badge-success {
                background: rgba(16, 185, 129, 0.1);
                color: var(--success);
                border: 1px solid rgba(16, 185, 129, 0.2);
            }
            
            .badge-warning {
                background: rgba(245, 158, 11, 0.1);
                color: var(--warning);
                border: 1px solid rgba(245, 158, 11, 0.2);
            }
            
            .badge-error {
                background: rgba(239, 68, 68, 0.1);
                color: var(--error);
                border: 1px solid rgba(239, 68, 68, 0.2);
            }
            
            .badge-info {
                background: rgba(14, 165, 233, 0.1);
                color: var(--info);
                border: 1px solid rgba(14, 165, 233, 0.2);
            }
            
            /* Duty rate tags */
            .duty-tag {
                display: inline-block;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 700;
                margin-right: 6px;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            
            .duty-free { background: rgba(16, 185, 129, 0.15); color: #10b981; }
            .duty-low { background: rgba(59, 130, 246, 0.15); color: #3b82f6; }
            .duty-medium { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
            .duty-high { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
            
            /* ============================================================================ */
            /* CONFIDENCE INDICATORS */
            /* ============================================================================ */
            
            .confidence-badge {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 8px 14px;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 600;
                backdrop-filter: blur(8px);
            }
            
            .confidence-high {
                background: rgba(16, 185, 129, 0.1);
                color: #059669;
                border: 1px solid rgba(16, 185, 129, 0.2);
            }
            
            .confidence-medium {
                background: rgba(99, 102, 241, 0.1);
                color: #4f46e5;
                border: 1px solid rgba(99, 102, 241, 0.2);
            }
            
            .confidence-low {
                background: rgba(245, 158, 11, 0.1);
                color: #d97706;
                border: 1px solid rgba(245, 158, 11, 0.2);
            }
            
            .confidence-very-low {
                background: rgba(244, 63, 94, 0.1);
                color: #e11d48;
                border: 1px solid rgba(244, 63, 94, 0.2);
            }
            
            /* Progress bar for similarity */
            .similarity-bar {
                width: 100%;
                height: 8px;
                background: var(--bg-secondary);
                border-radius: 999px;
                overflow: hidden;
                margin-top: 12px;
            }
            
            .similarity-fill {
                height: 100%;
                border-radius: 999px;
                transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
                background: linear-gradient(90deg, var(--primary), var(--vibrant-green));
            }
            
            /* ============================================================================ */
            /* BUTTONS */
            /* ============================================================================ */
            
            .btn-primary {
                background: linear-gradient(135deg, var(--primary), var(--primary-vibrant));
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);
            }
            
            .btn-primary:hover {
                transform: translateY(-1px);
                box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.4);
            }
            
            .btn-secondary {
                background: white;
                color: var(--text-main);
                padding: 10px 20px;
                border-radius: 8px;
                border: 1px solid var(--border-light);
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            .btn-secondary:hover {
                border-color: var(--primary);
                color: var(--primary);
                transform: translateY(-1px);
            }
            
            /* ============================================================================ */
            /* ANIMATIONS */
            /* ============================================================================ */
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            @keyframes shimmer {
                0% { background-position: -1000px 0; }
                100% { background-position: 1000px 0; }
            }
            
            .animate-fade-in {
                animation: fadeIn 0.5s ease;
            }
            
            .animate-fade-in-up {
                animation: fadeInUp 0.6s ease;
            }
            
            /* ============================================================================ */
            /* RESULT CARDS */
            /* ============================================================================ */
            
            .result-card {
                background: white;
                border: 1px solid var(--border-light);
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                transition: all 0.2s ease;
            }
            
            .result-card:hover {
                border-color: var(--primary);
                transform: translateY(-2px);
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            }
            
            .result-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 16px;
            }
            
            .hts-code {
                font-size: 26px;
                font-weight: 800;
                color: var(--primary);
                letter-spacing: -0.02em;
            }
            
            .hts-title {
                font-size: 18px;
                font-weight: 600;
                color: var(--text-main);
                margin: 4px 0 12px 0;
                line-height: 1.4;
            }
            
            .hts-description {
                font-size: 14px;
                color: var(--text-muted);
                line-height: 1.6;
                margin-top: 16px;
            }
            
            /* ============================================================================ */
            /* SIDEBAR ENHANCEMENTS */
            /* ============================================================================ */
            
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
            }
            
            [data-testid="stSidebar"] .element-container {
                transition: all 0.2s ease;
            }
            
            /* ============================================================================ */
            /* UTILITY CLASSES */
            /* ============================================================================ */
            
            .text-gradient {
                background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .text-muted {
                color: var(--text-muted);
            }
            
            .text-accent {
                color: var(--accent-primary);
            }
            
            .mt-4 { margin-top: 16px; }
            .mb-4 { margin-bottom: 16px; }
            .p-4 { padding: 16px; }
            
            /* ============================================================================ */
            /* RESPONSIVE DESIGN */
            /* ============================================================================ */
            
            @media (max-width: 768px) {
                .hero-title {
                    font-size: 36px;
                }
                
                .section-title {
                    font-size: 24px;
                }
                
                .glass-card, .glass-card-premium {
                    padding: 16px;
                }
            }
        </style>
        """),
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str | None = None, icon: str = "") -> None:
    """Render an enhanced page header with optional icon and subtitle."""
    icon_html = f'<span style="margin-right: 12px;">{icon}</span>' if icon else ""
    
    st.markdown(
        textwrap.dedent(f"""
        <div class="animate-fade-in-up">
            <h1 class="hero-title">{icon_html}{title}</h1>
            {f'<p class="subtitle">{subtitle}</p>' if subtitle else ''}
        </div>
        """),
        unsafe_allow_html=True,
    )


def glass_card(content: str, premium: bool = False) -> None:
    """Render a glassmorphism card with content."""
    card_class = "glass-card-premium" if premium else "glass-card"
    st.markdown(
        f'<div class="{card_class} animate-fade-in">{content}</div>',
        unsafe_allow_html=True,
    )


def feature_card(icon: str, title: str, description: str, extra: str = "") -> None:
    """Render a feature card with icon, title, and description."""
    content = textwrap.dedent(f"""
        <div style="text-align: left;">
            <div style="font-size: 48px; margin-bottom: 16px;">{icon}</div>
            <h3 style="font-size: 20px; font-weight: 700; color: #fff; margin-bottom: 8px;">
                {title}
            </h3>
            <p style="font-size: 14px; color: rgba(255, 255, 255, 0.7); line-height: 1.6; margin-bottom: 0;">
                {description}
            </p>
            {f'<div style="margin-top: 12px; font-size: 12px; color: rgba(255, 255, 255, 0.5);">{extra}</div>' if extra else ''}
        </div>
    """).strip()
    glass_card(content, premium=False)


def confidence_badge(score: float) -> str:
    """Generate HTML for a confidence badge based on similarity score."""
    percentage = int(score * 100)
    
    if percentage >= 90:
        badge_class = "confidence-high"
        icon = "✓"
        label = "Excellent Match"
    elif percentage >= 75:
        badge_class = "confidence-medium"
        icon = "~"
        label = "Good Match"
    elif percentage >= 60:
        badge_class = "confidence-low"
        icon = "!"
        label = "Fair Match"
    else:
        badge_class = "confidence-very-low"
        icon = "?"
        label = "Weak Match"
    
    return textwrap.dedent(f"""
        <div class="confidence-badge {badge_class}">
            <span style="font-size: 16px;">{icon}</span>
            <span>{percentage}% - {label}</span>
        </div>
    """).strip()


def similarity_bar(score: float) -> str:
    """Generate HTML for a similarity progress bar."""
    percentage = int(score * 100)
    return textwrap.dedent(f"""
        <div class="similarity-bar">
            <div class="similarity-fill" style="width: {percentage}%;"></div>
        </div>
    """).strip()


def duty_tag(rate: str) -> str:
    """Generate HTML for a duty rate tag."""
    duty_classes = {
        "Free": "duty-free",
        "Low": "duty-low",
        "Medium": "duty-medium",
        "High": "duty-high",
    }
    
    duty_class = duty_classes.get(rate, "duty-medium")
    return f'<span class="duty-tag {duty_class}">{rate} Duty</span>'


def result_card(
    hts_code: str,
    title: str,
    description: str,
    similarity: float = 0.0,
    duty_rate: str = "",
    show_explain: bool = False,
) -> None:
    """Render an enhanced result card with glassmorphism."""
    
    confidence_html = confidence_badge(similarity) if similarity > 0 else ""
    similarity_html = similarity_bar(similarity) if similarity > 0 else ""
    duty_html = duty_tag(duty_rate) if duty_rate else ""
    
    explain_button = ""
    if show_explain:
        explain_button = textwrap.dedent("""
            <button class="btn-secondary" style="margin-top: 12px; font-size: 13px; padding: 8px 16px;">
                🤖 Explain this classification
            </button>
        """).strip()
    
    content = textwrap.dedent(f"""
        <div class="result-header">
            <div>
                <div class="hts-code">{hts_code}</div>
                <div class="hts-title">{title}</div>
                {f'<div style="margin-top: 8px;">{duty_html}</div>' if duty_html else ''}
            </div>
            <div>
                {confidence_html}
            </div>
        </div>
        {similarity_html}
        <details style="margin-top: 16px;">
            <summary style="cursor: pointer; color: var(--text-muted); font-size: 14px;">
                Show full description
            </summary>
            <div class="hts-description">{description}</div>
        </details>
        {explain_button}
    """).strip()
    
    st.markdown(
        f'<div class="result-card">{content}</div>',
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, icon: str = "📊") -> None:
    """Render a metric card with glassmorphism."""
    content = textwrap.dedent(f"""
        <div style="text-align: center;">
            <div style="font-size: 36px; margin-bottom: 8px;">{icon}</div>
            <div style="font-size: 32px; font-weight: 700; color: var(--primary); margin-bottom: 4px;">
                {value}
            </div>
            <div style="font-size: 14px; color: var(--text-muted);">
                {label}
            </div>
        </div>
    """).strip()
    glass_card(content, premium=False)
