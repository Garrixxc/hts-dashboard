import streamlit as st
import textwrap
from utils.supabase_db import supabase
from utils.ui import inject_global_css, page_header, glass_card

st.set_page_config(
    page_title="Chunk Browser - HTS Dashboard",
    page_icon="🔍",
    layout="wide",
)

inject_global_css()

page_header(
    "Knowledge Base Explorer",
    "Advanced granular access to the vectorized HTS schedule. Monitor embedding health and text-to-vector alignment.",
    icon="💾"
)

# Search and filter controls
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    search_query = st.text_input(
        "🔎 Search Chunks",
        placeholder="Search by HTS code, title, or content...",
        help="Full-text search across all chunk fields"
    )

with col2:
    limit = st.selectbox(
        "Results per page",
        options=[10, 25, 50, 100],
        index=2,
        help="Number of chunks to display"
    )

with col3:
    st.markdown("###")  # Spacing
    search_button = st.button("🔍 Search", type="primary", use_container_width=True)

# Advanced filters
with st.expander("🔧 Advanced Filters", expanded=False):
    col_a, col_b = st.columns(2)
    
    with col_a:
        hts_code_filter = st.text_input(
            "Filter by HTS Code",
            placeholder="e.g., 3923, 0101",
            help="Show only chunks matching this code pattern"
        )
    
    with col_b:
        chapter_filter = st.text_input(
            "Filter by Chapter",
            placeholder="e.g., 39 (Plastics)",
            help="Show only chunks from this chapter"
        )

st.markdown("<br>", unsafe_allow_html=True)

# Fetch and display chunks
if search_button or 'chunks_loaded' not in st.session_state:
    st.session_state['chunks_loaded'] = True
    
    with st.spinner("📚 Loading chunks from database..."):
        try:
            # Build query
            query = supabase.table("hts_knowledge_chunks").select("*")
            
            # Apply filters
            if search_query:
                # Search across multiple fields
                query = query.or_(f"hts_code.ilike.%{search_query}%,title.ilike.%{search_query}%,normalized_text.ilike.%{search_query}%")
            
            if hts_code_filter:
                query = query.ilike("hts_code", f"%{hts_code_filter}%")
            
            if chapter_filter:
                query = query.ilike("hts_code", f"{chapter_filter}%")
            
            # Execute query
            response = query.limit(limit).execute()
            chunks = response.data
            
            if not chunks:
                st.warning("No chunks found matching your criteria. Try different filters.")
            else:
                st.markdown("---")
                st.markdown(
                    f'<h2 class="section-title">📚 Knowledge Chunks</h2>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<p class="subtitle">Showing {len(chunks)} chunks from the database</p>',
                    unsafe_allow_html=True
                )
                
                # Display chunks
                for idx, chunk in enumerate(chunks):
                    with st.expander(
                        f"#{idx+1}: {chunk.get('hts_code', 'N/A')} - {chunk.get('title', 'Untitled')[:80]}",
                        expanded=False
                    ):
                        # Chunk details
                        col_info, col_meta = st.columns([3, 1])
                        
                        with col_info:
                            st.markdown(f"### {chunk.get('hts_code', 'N/A')}")
                            st.markdown(f"**Title:** {chunk.get('title', 'N/A')}")
                            
                            st.markdown("**Content:**")
                            content = chunk.get('normalized_text', 'No content available')
                            st.markdown(
                                textwrap.dedent(f"""
                                <div class="glass-card" style="padding: 16px; margin-top: 8px;">
                                    <p style="font-size: 14px; line-height: 1.6; color: rgba(255, 255, 255, 0.8); margin: 0;">
                                        {content[:500]}{'...' if len(content) > 500 else ''}
                                    </p>
                                </div>
                                """),
                                unsafe_allow_html=True
                            )
                        
                        with col_meta:
                            st.markdown("**Metadata**")
                            
                            # Display metadata
                            metadata_html = textwrap.dedent(f"""
                            <div class="glass-card" style="padding: 12px; font-size: 13px;">
                                <p><strong>ID:</strong> {chunk.get('id', 'N/A')}</p>
                                <p><strong>Has Embedding:</strong> {'✅ Yes' if chunk.get('embedding') else '❌ No'}</p>
                                <p><strong>Embedding Dim:</strong> {len(chunk.get('embedding', [])) if chunk.get('embedding') else 'N/A'}</p>
                            </div>
                            """).strip()
                            st.markdown(metadata_html, unsafe_allow_html=True)
                        
                        # Action buttons
                        st.markdown("<br>", unsafe_allow_html=True)
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            if st.button("📋 Copy Code", key=f"copy_{idx}", use_container_width=True):
                                st.code(chunk.get('hts_code', ''), language=None)
                        
                        with col2:
                            if st.button("📄 Full Text", key=f"full_{idx}", use_container_width=True):
                                st.text_area(
                                    "Full Content",
                                    value=content,
                                    height=200,
                                    key=f"text_{idx}"
                                )
                        
                        with col3:
                            if st.button("🔍 Search Similar", key=f"similar_{idx}", use_container_width=True):
                                st.info(f"Navigate to HTS Search and search for: {chunk.get('hts_code', '')}")
                        
                        with col4:
                            if st.button("📊 View Stats", key=f"stats_{idx}", use_container_width=True):
                                st.json({
                                    "id": chunk.get('id'),
                                    "hts_code": chunk.get('hts_code'),
                                    "title_length": len(chunk.get('title', '')),
                                    "content_length": len(chunk.get('normalized_text', '')),
                                    "has_embedding": bool(chunk.get('embedding'))
                                })
                
                # Pagination info
                st.markdown("---")
                st.info(f"💡 Showing {len(chunks)} of potentially more chunks. Adjust filters or increase limit to see more.")
        
        except Exception as e:
            st.error(f"❌ Error loading chunks: {str(e)}")
            st.info("Make sure your Supabase connection is configured correctly.")

# Sidebar info
with st.sidebar:
    st.markdown("### 📚 About Chunk Browser")
    
    st.markdown(
        textwrap.dedent("""
        <div class="glass-card">
            <p style="font-size: 14px; line-height: 1.6; color: var(--text-main);">
                The <strong>Chunk Browser</strong> lets you explore the raw knowledge base 
                that powers semantic search and classification.
            </p>
            <br>
            <p style="font-size: 14px; line-height: 1.6; color: var(--text-muted);">
                Each "chunk" is a piece of HTS documentation with:
            </p>
            <ul style="font-size: 13px; line-height: 1.8; color: var(--text-muted);">
                <li>HTS code</li>
                <li>Title/description</li>
                <li>Full text content</li>
                <li>Vector embedding</li>
            </ul>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(
        textwrap.dedent("""
        <div class="glass-card">
            <h4 style="color: var(--accent-primary); margin-bottom: 12px;">Use Cases:</h4>
            <ul style="font-size: 13px; line-height: 1.8; color: var(--text-muted);">
                <li>Debug search results</li>
                <li>Explore HTS structure</li>
                <li>Verify embeddings</li>
                <li>Find data gaps</li>
                <li>Quality assurance</li>
            </ul>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(
        textwrap.dedent("""
        <div class="glass-card">
            <h4 style="color: var(--accent-secondary); margin-bottom: 12px;">Quick Stats:</h4>
            <ul style="font-size: 13px; line-height: 1.8; color: var(--text-muted);">
                <li>📊 35,000+ total chunks</li>
                <li>🔢 1536-dim embeddings</li>
                <li>⚡ Real-time search</li>
                <li>🎯 Full-text filtering</li>
            </ul>
        </div>
        """),
        unsafe_allow_html=True
    )
