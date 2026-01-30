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
                /* Primary Colors - Vibrant & Bright */
                --accent-primary: #4f46e5;    /* Indigo-600 */
                --accent-secondary: #f59e0b;  /* Amber-500 */
                --accent-vibrant: #10b981;    /* Emerald-500 */
                --accent-stone: #64748b;      /* Slate-500 */
                
                /* Semantic Colors */
                --success: #059669;          /* Emerald-600 */
                --warning: #d97706;          /* Amber-600 */
                --error: #dc2626;            /* Red-600 */
                --info: #2563eb;             /* Blue-600 */
                
                /* Backgrounds - Crisp Light */
                --bg-main: #f8fafc;          /* Slate-50 */
                --bg-card: #ffffff;          /* Pure White */
                --bg-glass: rgba(255, 255, 255, 0.9);
                --bg-glass-hover: #ffffff;
                
                /* Borders */
                --border-subtle: #e2e8f0;    /* Slate-200 */
                --border-medium: #cbd5e1;    /* Slate-300 */
                
                /* Shadows - Soft & Clean */
                --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
                --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
                --shadow-premium: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                
                /* Typography - Dark Contrast */
                --font-heading: 'Inter', -apple-system, sans-serif;
                --font-body: 'Inter', -apple-system, sans-serif;
                --text-main: #0f172a;        /* Slate-900 */
                --text-muted: #475569;      /* Slate-600 */
            }
            
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

            /* Global Streamlit Reset to Light */
            .main, .stApp {
                background-color: var(--bg-main) !important;
                color: var(--text-main) !important;
            }
            
            .stMarkdown, .stText, p, span, li, label {
                color: var(--text-main) !important;
            }

            .main {
                background-color: var(--bg-main);
                background-image: 
                    radial-gradient(at 0% 0%, rgba(79, 70, 229, 0.05) 0, transparent 50%), 
                    radial-gradient(at 50% 0%, rgba(245, 158, 11, 0.03) 0, transparent 50%);
            }
            
            .gradient-bg {
                background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
                border: 1px solid var(--border-subtle);
                border-top: 2px solid var(--accent-primary);
            }
            
            /* ============================================================================ */
            /* GLASSMORPHISM COMPONENTS (Now Light Mode) */
            /* ============================================================================ */
            
            .glass-card {
                background: var(--bg-card);
                border: 1px solid var(--border-subtle);
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 16px;
                box-shadow: var(--shadow-md);
                transition: all 0.2s ease-in-out;
            }
            
            .glass-card:hover {
                border-color: var(--accent-primary);
                box-shadow: var(--shadow-lg);
                transform: translateY(-2px);
            }
            
            .glass-card-premium {
                background: var(--bg-card);
                border: 1px solid var(--border-subtle);
                border-radius: 16px;
                padding: 28px;
                margin-bottom: 20px;
                box-shadow: var(--shadow-premium);
                position: relative;
                overflow: hidden;
            }
            
            .glass-card-premium::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            }
            
            /* ============================================================================ */
            /* TYPOGRAPHY */
            /* ============================================================================ */
            
            .hero-title {
                font-family: var(--font-heading);
                font-size: 48px;
                font-weight: 800;
                color: var(--text-main);
                margin-bottom: 12px;
                letter-spacing: -0.02em;
            }
            
            .section-title {
                font-family: var(--font-heading);
                font-size: 24px;
                font-weight: 700;
                color: var(--text-main);
                margin-bottom: 16px;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .subtitle {
                font-size: 18px;
                color: var(--text-muted);
                margin-bottom: 32px;
                line-height: 1.6;
                font-weight: 400;
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
                background: rgba(6, 255, 165, 0.2);
                color: var(--success);
                border: 1px solid rgba(6, 255, 165, 0.4);
            }
            
            .confidence-medium {
                background: rgba(76, 201, 240, 0.2);
                color: var(--info);
                border: 1px solid rgba(76, 201, 240, 0.4);
            }
            
            .confidence-low {
                background: rgba(255, 214, 10, 0.2);
                color: var(--warning);
                border: 1px solid rgba(255, 214, 10, 0.4);
            }
            
            .confidence-very-low {
                background: rgba(239, 71, 111, 0.2);
                color: var(--error);
                border: 1px solid rgba(239, 71, 111, 0.4);
            }
            
            /* Progress bar for similarity */
            .similarity-bar {
                width: 100%;
                height: 6px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 999px;
                overflow: hidden;
                margin-top: 8px;
            }
            
            .similarity-fill {
                height: 100%;
                border-radius: 999px;
                transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
                background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
            }
            
            /* ============================================================================ */
            /* BUTTONS */
            /* ============================================================================ */
            
            .btn-primary {
                background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: var(--shadow-sm);
            }
            
            .btn-primary:hover {
                filter: brightness(1.1);
                transform: translateY(-1px);
                box-shadow: var(--shadow-md);
            }
            
            .btn-secondary {
                background: var(--bg-glass);
                backdrop-filter: blur(10px);
                color: white;
                padding: 12px 24px;
                border-radius: 12px;
                border: 1px solid var(--border-subtle);
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .btn-secondary:hover {
                background: var(--bg-glass-hover);
                border-color: var(--border-medium);
                transform: translateY(-2px);
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
                background: var(--bg-card);
                border: 1px solid var(--border-subtle);
                border-top: 1px solid var(--border-medium);
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 16px;
                transition: all 0.2s ease-in-out;
            }
            
            .result-card:hover {
                border-color: var(--accent-primary);
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg);
            }
            
            .result-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 12px;
            }
            
            .hts-code {
                font-size: 24px;
                font-weight: 700;
                color: var(--accent-blue);
                font-family: var(--font-mono);
            }
            
            .hts-title {
                font-size: 16px;
                color: rgba(255, 255, 255, 0.9);
                margin: 8px 0;
                line-height: 1.5;
            }
            
            .hts-description {
                font-size: 14px;
                color: rgba(255, 255, 255, 0.6);
                line-height: 1.6;
                margin-top: 12px;
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
            <div style="font-size: 32px; font-weight: 700; color: var(--accent-primary); margin-bottom: 4px;">
                {value}
            </div>
            <div style="font-size: 14px; color: var(--text-muted);">
                {label}
            </div>
        </div>
    """).strip()
    glass_card(content, premium=False)
