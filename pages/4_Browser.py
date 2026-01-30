import streamlit as st
import textwrap
from utils.supabase_db import get_hts_page, count_hts_rows
from utils.ui import inject_global_css, page_header, glass_card, result_card
from utils.duty_rates import get_duty_category

st.set_page_config(
    page_title="HTS Browser - HTS Dashboard",
    page_icon="📚",
    layout="wide",
)

inject_global_css()

page_header(
    "Regulatory Schedule Browser",
    "Comprehensive access to the complete 2026 HTS dataset. Explore legal headers, duty rates, and technical specifications."
)

# Get total count and calculate pages
total = count_hts_rows()
page_size = 20
total_pages = (total // page_size) + 1

# Page navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("### Navigation")

with col2:
    page = st.number_input(
        "Page Number",
        min_value=1,
        max_value=total_pages,
        value=1,
    )

with col3:
    st.markdown(f"### Total: {total:,} codes")

st.markdown("---")

# Fetch and display rows
rows = get_hts_page(page=page, page_size=page_size)

st.markdown(f"## Page {page} of {total_pages}")
st.markdown(f"Showing {len(rows)} HTS codes from the database")

# Display each row
for idx, r in enumerate(rows):
    duty_category = get_duty_category(r['hts_code'])
    
    result_card(
        hts_code=r['hts_code'],
        title=r['title'],
        description=r.get('normalized_text', 'No additional details available'),
        duty_rate=duty_category,
    )

# Pagination controls
st.markdown("---")

col_prev, col_info, col_next = st.columns([1, 2, 1])

with col_prev:
    if page > 1:
        if st.button("← Previous Page", use_container_width=True):
            st.rerun()

with col_info:
    st.markdown(f"<p style='text-align: center;'>Page {page} of {total_pages} • {total:,} total codes</p>", unsafe_allow_html=True)

with col_next:
    if page < total_pages:
        if st.button("Next Page →", use_container_width=True):
            st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### Browser Intelligence")
    st.info(f"""
    **Dataset Metrics:**
    - Compliance Depth: 2026
    - Total Declarations: {total:,}
    - Current View: Page {page}
    """)
    
    st.markdown("---")
    st.markdown("#### Navigation Tips")
    st.markdown("""
    - Use page number to jump directly
    - Click entries to expand details
    - Use HTS Search for specific queries
    """)
