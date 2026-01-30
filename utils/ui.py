import streamlit as st


def inject_global_css() -> None:
    """Inject shared CSS for all pages."""
    st.markdown(
        """
        <style>
            .main-title {
                font-size: 38px;
                font-weight: 700;
                padding: 0;
                margin-bottom: -4px;
            }
            .sub-text {
                font-size: 16px;
                opacity: 0.75;
                margin-bottom: 1.5rem;
            }
            .card {
                padding: 16px 18px;
                background-color: #161b22;
                border-radius: 12px;
                border: 1px solid #2f3542;
                margin-bottom: 12px;
            }
            .card h3 {
                margin-bottom: 4px;
                font-size: 18px;
            }
            .card p {
                margin-bottom: 0;
                opacity: 0.85;
                font-size: 14px;
            }
            .tag {
                display: inline-block;
                padding: 2px 8px;
                border-radius: 999px;
                background-color: #21262d;
                font-size: 11px;
                margin-right: 6px;
                margin-top: 4px;
                opacity: 0.9;
            }
            .metric-label {
                font-size: 12px;
                opacity: 0.7;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str | None = None) -> None:
    """Render a big title + optional subtitle."""
    st.markdown(f"<div class='main-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='sub-text'>{subtitle}</div>", unsafe_allow_html=True)


def card(title: str, body: str, extra: str | None = None) -> None:
    """Reusable card layout."""
    html = f"""
    <div class="card">
        <h3>{title}</h3>
        <p>{body}</p>
    """
    if extra:
        html += f"<div style='margin-top:6px;font-size:12px;opacity:0.7;'>{extra}</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
