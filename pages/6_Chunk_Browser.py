import streamlit as st
import textwrap
from utils.supabase_db import supabase
from utils.ui import inject_global_css, page_header

st.set_page_config(
    page_title="Chunk Browser - HTS Dashboard",
    page_icon="🔍",
    layout="wide",
)

inject_global_css()

page_header(
    "Knowledge Base Explorer",
    "Advanced granular access to the vectorized HTS schedule. Monitor embedding health and text-to-vector alignment."
)

# Search and filter controls
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    search_query = st.text_input(
        "Search Chunks",
        placeholder="Search by HTS code, title, or content...",
    )

with col2:
    limit = st.selectbox(
        "Results limit",
        options=[10, 25, 50, 100],
        index=2,
    )

with col3:
    st.markdown("###")  # Spacing
    search_button = st.button("Run Search", type="primary", use_container_width=True)

# Advanced filters
with st.expander("Advanced Filters", expanded=False):
    col_a, col_b = st.columns(2)
    
    with col_a:
        hts_code_filter = st.text_input(
            "Filter by HTS Code",
            placeholder="e.g., 3923",
        )
    
    with col_b:
        chapter_filter = st.text_input(
            "Filter by Chapter",
            placeholder="e.g., 39",
        )

st.markdown("<br>", unsafe_allow_html=True)

# Fetch and display chunks
if search_button or 'chunks_loaded' not in st.session_state:
    st.session_state['chunks_loaded'] = True
    
    with st.spinner("Loading chunks from database..."):
        try:
            # Build query
            query = supabase.table("hts_knowledge_chunks").select("*")
            
            # Apply filters
            if search_query:
                query = query.or_(f"hts_code.ilike.%{search_query}%,title.ilike.%{search_query}%,normalized_text.ilike.%{search_query}%")
            
            if hts_code_filter:
                query = query.ilike("hts_code", f"%{hts_code_filter}%")
            
            if chapter_filter:
                query = query.ilike("hts_code", f"{chapter_filter}%")
            
            # Execute query
            response = query.limit(limit).execute()
            chunks = response.data
            
            if not chunks:
                st.warning("No chunks found matching your criteria.")
            else:
                st.markdown(f"## Found {len(chunks)} Knowledge Chunks")
                
                # Display chunks
                for idx, chunk in enumerate(chunks):
                    with st.expander(
                        f"#{idx+1}: {chunk.get('hts_code', 'N/A')} - {chunk.get('title', 'Untitled')[:100]}",
                        expanded=False
                    ):
                        col_info, col_meta = st.columns([3, 1])
                        
                        with col_info:
                            st.markdown(f"### {chunk.get('hts_code', 'N/A')}")
                            st.info(f"**Title:** {chunk.get('title', 'N/A')}")
                            st.markdown("**Content Extract:**")
                            content = chunk.get('normalized_text', 'No content available')
                            st.markdown(f"> {content[:800]}...")
                        
                        with col_meta:
                            st.markdown("**Metadata**")
                            st.json({
                                "id": chunk.get('id'),
                                "embedding": "✅ 1536-dim" if chunk.get('embedding') else "❌ Missing"
                            })
                        
                        # Action buttons
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button("📋 Copy Code", key=f"copy_{idx}", use_container_width=True):
                                st.code(chunk.get('hts_code', ''), language=None)
                        with col_btn2:
                            if st.button("📄 Full Text", key=f"full_{idx}", use_container_width=True):
                                st.text_area("Full Content", value=content, height=200, key=f"text_{idx}")
                
                st.markdown("---")
                st.info(f"Showing {len(chunks)} results.")
        
        except Exception as e:
            st.error(f"Error loading chunks: {str(e)}")

# Sidebar info
with st.sidebar:
    st.markdown("### Knowledge Base Explorer")
    st.info("""
    The **Chunk Browser** lets you explore the raw knowledge base that powers semantic search.
    
    **Each chunk contains:**
    - HTS code alignment
    - Technical description
    - Vector embeddings
    """)
    
    st.markdown("---")
    st.markdown("#### Use Cases")
    st.markdown("""
    - Debug search results
    - Verify data integrity
    - Quality assurance
    - Data gap analysis
    """)
