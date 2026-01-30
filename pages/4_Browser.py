import streamlit as st
from utils.supabase_db import get_hts_page, count_hts_rows
from utils.ui import inject_global_css, page_header, glass_card
from utils.duty_rates import get_duty_category

st.set_page_config(
    page_title="HTS Browser - HTS Dashboard",
    page_icon="📚",
    layout="wide",
)

inject_global_css()

page_header(
    "HTS Code Browser",
    "Browse the complete HTS schedule page by page with detailed descriptions and metadata",
    icon="📚"
)

# Get total count and calculate pages
total = count_hts_rows()
page_size = 20
total_pages = (total // page_size) + 1

# Page navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("### 📄 Navigation")

with col2:
    page = st.number_input(
        "Page Number",
        min_value=1,
        max_value=total_pages,
        value=1,
        help=f"Browse through {total_pages} pages of HTS codes"
    )

with col3:
    st.markdown(f"### Total: {total:,} codes")

st.markdown("---")

# Fetch and display rows
rows = get_hts_page(page=page, page_size=page_size)

st.markdown(
    f'<h3 class="section-title" style="font-size: 20px;">📦 Page {page} of {total_pages}</h3>',
    unsafe_allow_html=True
)
st.markdown(
    f'<p class="subtitle">Showing {len(rows)} HTS codes from the database</p>',
    unsafe_allow_html=True
)

# Display each row as a glassmorphism card
for idx, r in enumerate(rows):
    duty_category = get_duty_category(r['hts_code'])
    
    # Duty tag HTML
    duty_classes = {
        "Free": "duty-free",
        "Low": "duty-low",
        "Medium": "duty-medium",
        "High": "duty-high",
    }
    duty_class = duty_classes.get(duty_category, "duty-medium")
    duty_tag_html = f'<span class="duty-tag {duty_class}">{duty_category} Duty</span>'
    
    content = f"""
    <div style="margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
            <div>
                <div class="hts-code">{r['hts_code']}</div>
                <div class="hts-title">{r['title']}</div>
            </div>
            <div>
                {duty_tag_html}
            </div>
        </div>
        <details style="margin-top: 12px;">
            <summary style="cursor: pointer; color: rgba(255, 255, 255, 0.7); font-size: 14px;">
                Show full description
            </summary>
            <div class="hts-description">{r.get('normalized_text', 'No additional details available')}</div>
        </details>
    </div>
    """
    
    st.markdown(
        f'<div class="result-card">{content}</div>',
        unsafe_allow_html=True
    )

# Pagination controls
st.markdown("---")

col_prev, col_info, col_next = st.columns([1, 2, 1])

with col_prev:
    if page > 1:
        if st.button("← Previous Page", use_container_width=True):
            st.rerun()

with col_info:
    st.markdown(
        f'<p style="text-align: center; color: rgba(255, 255, 255, 0.6);">Page {page} of {total_pages} • {total:,} total codes</p>',
        unsafe_allow_html=True
    )

with col_next:
    if page < total_pages:
        if st.button("Next Page →", use_container_width=True):
            st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### 📚 Browser Info")
    
    info = f"""
    <div class="glass-card">
        <p style="font-size: 14px; line-height: 1.6; color: rgba(255, 255, 255, 0.8);">
            The <strong>HTS Browser</strong> lets you browse all HTS codes sequentially, 
            perfect for exploring the complete schedule.
        </p>
        <br>
        <ul style="font-size: 13px; line-height: 1.8; color: rgba(255, 255, 255, 0.7);">
            <li><strong>Total Codes:</strong> {total:,}</li>
            <li><strong>Per Page:</strong> {page_size}</li>
            <li><strong>Total Pages:</strong> {total_pages:,}</li>
            <li><strong>Current Page:</strong> {page}</li>
        </ul>
    </div>
    """
    st.markdown(info, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    tips = """
    <div class="glass-card">
        <h4 style="color: var(--accent-blue); margin-bottom: 12px;">💡 Tips:</h4>
        <ul style="font-size: 13px; line-height: 1.8; color: rgba(255, 255, 255, 0.8);">
            <li>Use page number to jump directly</li>
            <li>Click details to expand descriptions</li>
            <li>Note duty rate categories</li>
            <li>Use Search for specific queries</li>
        </ul>
    </div>
    """
    st.markdown(tips, unsafe_allow_html=True)
