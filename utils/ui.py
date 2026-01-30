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
                /* Primary Colors */
                --accent-blue: #4cc9f0;
                --accent-purple: #7209b7;
                --accent-pink: #f72585;
                
                /* Semantic Colors */
                --success: #06ffa5;
                --warning: #ffd60a;
                --error: #ef476f;
                --info: #4cc9f0;
                
                /* Backgrounds */
                --bg-dark: #0d1117;
                --bg-card: #161b22;
                --bg-glass: rgba(255, 255, 255, 0.05);
                --bg-glass-hover: rgba(255, 255, 255, 0.08);
                
                /* Borders */
                --border-subtle: rgba(255, 255, 255, 0.1);
                --border-medium: rgba(255, 255, 255, 0.15);
                
                /* Shadows */
                --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
                --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
                --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
                --shadow-glow: 0 0 20px rgba(76, 201, 240, 0.3);
                
                /* Typography */
                --font-heading: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                --font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
            }
            
            /* ============================================================================ */
            /* GLOBAL STYLES */
            /* ============================================================================ */
            
            .main {
                background: linear-gradient(135deg, #0d1117 0%, #1a1f2e 100%);
            }
            
            /* Animated gradient background */
            .gradient-bg {
                background: linear-gradient(
                    135deg,
                    rgba(76, 201, 240, 0.1) 0%,
                    rgba(114, 9, 183, 0.1) 50%,
                    rgba(247, 37, 133, 0.1) 100%
                );
                background-size: 200% 200%;
                animation: gradientShift 15s ease infinite;
            }
            
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            /* ============================================================================ */
            /* GLASSMORPHISM COMPONENTS */
            /* ============================================================================ */
            
            .glass-card {
                background: var(--bg-glass);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid var(--border-subtle);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 16px;
                box-shadow: var(--shadow-md);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .glass-card:hover {
                background: var(--bg-glass-hover);
                border-color: var(--border-medium);
                box-shadow: var(--shadow-lg);
                transform: translateY(-2px);
            }
            
            .glass-card-premium {
                background: linear-gradient(
                    135deg,
                    rgba(76, 201, 240, 0.08) 0%,
                    rgba(114, 9, 183, 0.08) 100%
                );
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(76, 201, 240, 0.2);
                border-radius: 20px;
                padding: 28px;
                margin-bottom: 20px;
                box-shadow: var(--shadow-lg), var(--shadow-glow);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .glass-card-premium:hover {
                transform: translateY(-4px) scale(1.01);
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6), 0 0 30px rgba(76, 201, 240, 0.4);
            }
            
            /* ============================================================================ */
            /* TYPOGRAPHY */
            /* ============================================================================ */
            
            .hero-title {
                font-size: 56px;
                font-weight: 800;
                background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 16px;
                line-height: 1.2;
                animation: fadeInUp 0.8s ease;
            }
            
            .section-title {
                font-size: 32px;
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .subtitle {
                font-size: 18px;
                color: rgba(255, 255, 255, 0.7);
                margin-bottom: 32px;
                line-height: 1.6;
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
                background: rgba(6, 255, 165, 0.15);
                color: var(--success);
                border: 1px solid rgba(6, 255, 165, 0.3);
            }
            
            .badge-warning {
                background: rgba(255, 214, 10, 0.15);
                color: var(--warning);
                border: 1px solid rgba(255, 214, 10, 0.3);
            }
            
            .badge-error {
                background: rgba(239, 71, 111, 0.15);
                color: var(--error);
                border: 1px solid rgba(239, 71, 111, 0.3);
            }
            
            .badge-info {
                background: rgba(76, 201, 240, 0.15);
                color: var(--info);
                border: 1px solid rgba(76, 201, 240, 0.3);
            }
            
            /* Duty rate tags */
            .duty-tag {
                display: inline-block;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                margin-right: 6px;
            }
            
            .duty-free { background: rgba(6, 255, 165, 0.2); color: var(--success); }
            .duty-low { background: rgba(76, 201, 240, 0.2); color: var(--info); }
            .duty-medium { background: rgba(255, 214, 10, 0.2); color: var(--warning); }
            .duty-high { background: rgba(239, 71, 111, 0.2); color: var(--error); }
            
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
                background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
                color: white;
                padding: 12px 24px;
                border-radius: 12px;
                border: none;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: var(--shadow-md);
            }
            
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg), var(--shadow-glow);
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
                background: var(--bg-glass);
                backdrop-filter: blur(10px);
                border: 1px solid var(--border-subtle);
                border-radius: 16px;
                padding: 20px;
                margin-bottom: 16px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                animation: fadeInUp 0.4s ease;
            }
            
            .result-card:hover {
                background: var(--bg-glass-hover);
                border-color: var(--accent-blue);
                transform: translateX(4px);
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
                background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .text-muted {
                color: rgba(255, 255, 255, 0.6);
            }
            
            .text-accent {
                color: var(--accent-blue);
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
            <summary style="cursor: pointer; color: rgba(255, 255, 255, 0.7); font-size: 14px;">
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
            <div style="font-size: 32px; font-weight: 700; color: var(--accent-blue); margin-bottom: 4px;">
                {value}
            </div>
            <div style="font-size: 14px; color: rgba(255, 255, 255, 0.6);">
                {label}
            </div>
        </div>
    """).strip()
    glass_card(content, premium=False)
