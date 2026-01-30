import streamlit as st
from utils.ui import inject_global_css, page_header, card

st.set_page_config(
    page_title="HTS Intelligence Dashboard",
    page_icon="📦",
    layout="wide",
)

inject_global_css()

page_header(
    "📦 HTS Intelligence Dashboard",
    "AI-accelerated search, classification, and exploration of the full HTS dataset.",
)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🚀 What you can do here")
    card(
        "🔍 HTS Search",
        "Semantic search across 35k+ HTS records. Type plain English or a code like '0101'.",
        "Use it when you know roughly what you’re looking for and want the closest matches.",
    )
    card(
        "🧠 Classification AI",
        "Paste a product description and get top candidate HTS codes.",
        "Great for customs, trade compliance, or sanity-checking an existing classification.",
    )
    card(
        "📚 HTS Browser",
        "Browse the HTS hierarchy page by page.",
        "Useful for exploring nearby headings, footnotes, and wording nuance.",
    )
    card(
        "📊 Analytics",
        "See how you’re using the tool over time.",
        "Perfect for spotting common queries and training needs.",
    )

with col2:
    st.markdown("### 💡 How to use it effectively")
    st.markdown(
        """
        - Start with **HTS Search** and try a few example queries  
        - When classifying a product, write **rich descriptions**:
          - what it’s made of  
          - how it’s used  
          - key technical specs  
        - Use **Browser** to read the legal text around any candidate code  
        - Re-run **Classification AI** with improved wording if needed  
        """
    )

st.markdown("---")
st.caption("Tip: use the sidebar on the left to switch between tools.")
