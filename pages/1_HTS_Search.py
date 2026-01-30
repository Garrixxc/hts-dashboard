import streamlit as st
import textwrap
from utils.search import semantic_search_hts
from utils.ui import inject_global_css, page_header, result_card
from utils.duty_rates import get_duty_category

st.set_page_config(
    page_title="HTS Search - HTS Dashboard",
    page_icon="🔍",
    layout="wide",
)

inject_global_css()

page_header(
    "Customs Intelligence Search",
    "On-demand semantic access to the complete 35,571 record HTS database. Identify precise classifications through technical context matching.",
    icon="🔍"
)

# Quick examples
st.markdown("### Try These Examples")

examples = [
    ("Live purebred horses", "🐴"),
    ("PET beverage containers", "🍾"),
    ("Coaxial cable connectors", "🔌"),
    ("Knitted cotton t-shirts", "👕"),
    ("Glazed ceramic tiles", "🏠"),
]

cols = st.columns(len(examples))
for i, (ex, emoji) in enumerate(examples):
    if cols[i].button(f"{emoji} {ex.title()}", key=f"ex_{i}", use_container_width=True):
        st.session_state["query"] = ex

st.markdown("<br>", unsafe_allow_html=True)

# Search interface
col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_input(
        "Search Query",
        value=st.session_state.get("query", ""),
        placeholder="e.g., 'stainless steel screws', '0101', 'electric motors', 'plastic containers'",
        help="Enter a product description, HTS code fragment, or keywords"
    )

with col2:
    st.markdown("### Options")
    k = st.slider(
        "Results",
        min_value=1,
        max_value=20,
        value=10,
    )

# Advanced filters
with st.expander("Advanced Filters", expanded=False):
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        min_similarity = st.slider(
            "Minimum Confidence",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
        )
    
    with col_b:
        duty_filter = st.multiselect(
            "Duty Categories",
            options=["Free", "Low", "Medium", "High"],
            default=[],
        )
    
    with col_c:
        sort_by = st.selectbox(
            "Sort By",
            options=["Relevance", "HTS Code", "Duty Rate"],
        )

st.markdown("<br>", unsafe_allow_html=True)

# Search button
search_button = st.button("Search Database", type="primary")

# Search logic
if search_button:
    if not query.strip():
        st.error("Please enter a search query")
    else:
        with st.spinner("Searching HTS database..."):
            results = semantic_search_hts(query, k)
        
        if not results:
            st.warning("No results found. Try different keywords or broader terms.")
        else:
            # Apply filters
            filtered_results = results
            
            # Filter by similarity
            filtered_results = [r for r in filtered_results if r.get('similarity', 0.85) >= min_similarity]
            
            # Filter by duty category
            if duty_filter:
                filtered_results = [
                    r for r in filtered_results
                    if get_duty_category(r['hts_code']) in duty_filter
                ]
            
            # Sort results
            if sort_by == "HTS Code":
                filtered_results.sort(key=lambda x: x['hts_code'])
            elif sort_by == "Duty Rate":
                duty_order = {"Free": 0, "Low": 1, "Medium": 2, "High": 3}
                filtered_results.sort(key=lambda x: duty_order.get(get_duty_category(x['hts_code']), 2))
            
            st.markdown("---")
            st.markdown(f"## Found {len(filtered_results)} matches for '{query}'")
            
            if len(filtered_results) == 0:
                st.info("No results match your filters. Try adjusting the filter criteria.")
            else:
                for idx, r in enumerate(filtered_results):
                    similarity = r.get('similarity', 0.85)
                    duty_category = get_duty_category(r['hts_code'])
                    
                    result_card(
                        hts_code=r['hts_code'],
                        title=r['title'],
                        description=r.get('normalized_text', 'No additional details available'),
                        similarity=similarity,
                        duty_rate=duty_category,
                    )

# Sidebar info
with st.sidebar:
    st.markdown("### Search Intelligence")
    st.info("""
    **How Search Works:**
    Our AI understands context and meaning, not just keywords. It identifies technical synonyms and industrial applications.
    """)
    
    st.markdown("---")
    st.markdown("#### Search Strategies")
    st.markdown("""
    - **Broad terms** for exploration
    - **Specific materials** for precision
    - **Use cases** for applications
    - **Code fragments** like '3923'
    """)
    
    st.markdown("---")
    st.markdown("#### Database Coverage")
    st.markdown("""
    - 📚 35,000+ HTS codes
    - 🔍 Semantic matching
    - ⚡ Sub-2s response
    """)
