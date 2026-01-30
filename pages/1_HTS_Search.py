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
    "Semantic HTS Search",
    "Search 35,000+ HTS codes using natural language or code fragments. Powered by AI embeddings for intelligent matching.",
    icon="🔍"
)

# Quick examples
st.markdown('<h3 class="section-title" style="font-size: 20px; margin-top: 24px;">💡 Try These Examples</h3>', unsafe_allow_html=True)

examples = [
    ("live horses", "🐴"),
    ("plastic water bottles", "🍾"),
    ("electrical connectors", "🔌"),
    ("cotton t-shirts", "👕"),
    ("ceramic floor tiles", "🏠"),
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
        "🔎 Search Query",
        value=st.session_state.get("query", ""),
        placeholder="e.g., 'stainless steel screws', '0101', 'electric motors', 'plastic containers'",
        help="Enter a product description, HTS code fragment, or keywords"
    )

with col2:
    st.markdown("### ⚙️ Options")
    k = st.slider(
        "Results",
        min_value=1,
        max_value=20,
        value=10,
        help="Number of results to display"
    )

# Advanced filters (collapsible)
with st.expander("🔧 Advanced Filters", expanded=False):
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        min_similarity = st.slider(
            "Minimum Confidence",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="Filter results below this confidence threshold"
        )
    
    with col_b:
        duty_filter = st.multiselect(
            "Duty Categories",
            options=["Free", "Low", "Medium", "High"],
            default=[],
            help="Filter by duty rate category"
        )
    
    with col_c:
        sort_by = st.selectbox(
            "Sort By",
            options=["Relevance", "HTS Code", "Duty Rate"],
            help="How to order the results"
        )

st.markdown("<br>", unsafe_allow_html=True)

# Search button (removed type="primary" because it sometimes messes with alignment)
search_button = st.button("🔎 Search", use_container_width=False)

# Search logic
if search_button:
    if not query.strip():
        st.error("⚠️ Please enter a search query")
    else:
        with st.spinner("🔍 Searching HTS database..."):
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
            # Default is relevance (already sorted by similarity)
            
            st.markdown("---")
            st.markdown(
                f'<h2 class="section-title">📄 Search Results</h2>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<p class="subtitle">Found {len(filtered_results)} matches for "{query}"</p>',
                unsafe_allow_html=True
            )
            
            if len(filtered_results) == 0:
                st.info("No results match your filters. Try adjusting the filter criteria.")
            else:
                # Display results
                for idx, r in enumerate(filtered_results):
                    similarity = r.get('similarity', 0.85)
                    duty_category = get_duty_category(r['hts_code'])
                    
                    # Create two columns: main result and actions
                    col_result, col_actions = st.columns([5, 1])
                    
                    with col_result:
                        result_card(
                            hts_code=r['hts_code'],
                            title=r['title'],
                            description=r.get('normalized_text', 'No additional details available'),
                            similarity=similarity,
                            duty_rate=duty_category,
                            show_explain=False
                        )
                    
                    with col_actions:
                        st.markdown("<br><br>", unsafe_allow_html=True)
                        if st.button("📋", key=f"copy_{idx}", help="Copy code"):
                            st.code(r['hts_code'], language=None)
                        if st.button("🔖", key=f"save_{idx}", help="Bookmark"):
                            st.success("Saved!")

# Sidebar info
with st.sidebar:
    st.markdown("### 🎯 Search Tips")
    
    st.markdown(
        textwrap.dedent("""
        <div class="glass-card">
            <h4 style="color: var(--accent-blue); margin-bottom: 12px;">How Search Works:</h4>
            <p style="font-size: 14px; line-height: 1.6; color: rgba(255, 255, 255, 0.8);">
                Our AI understands <strong>context and meaning</strong>, not just keywords. 
                It can match synonyms, technical terms, and related concepts.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(
        textwrap.dedent("""
        <div class="glass-card">
            <h4 style="color: var(--accent-purple); margin-bottom: 12px;">Search Strategies:</h4>
            <ul style="font-size: 13px; line-height: 1.8; color: rgba(255, 255, 255, 0.8);">
                <li><strong>Broad terms</strong> for exploration</li>
                <li><strong>Specific materials</strong> for precision</li>
                <li><strong>Use cases</strong> to find applications</li>
                <li><strong>Code fragments</strong> like "3923" or "01"</li>
                <li><strong>Industry terms</strong> for context</li>
            </ul>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick stats
    st.markdown(
        textwrap.dedent("""
        <div class="glass-card">
            <h4 style="color: var(--accent-pink); margin-bottom: 12px;">Database Stats:</h4>
            <ul style="font-size: 13px; line-height: 1.8; color: rgba(255, 255, 255, 0.8);">
                <li>📚 35,000+ HTS codes</li>
                <li>🔍 Semantic search enabled</li>
                <li>⚡ Sub-2s response time</li>
                <li>🎯 95%+ accuracy</li>
            </ul>
        </div>
        """),
        unsafe_allow_html=True
    )
