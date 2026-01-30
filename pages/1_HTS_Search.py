import streamlit as st
from utils.search import semantic_search_hts

st.title("🔍 HTS Semantic Search")
st.write("Search the HTS database using AI-powered semantic search.")

st.markdown("### 💡 Try Examples:")
examples = [
    "live horses",
    "plastic water bottles",
    "electrical connectors",
    "cotton t-shirts",
    "ceramic floor tiles",
]

cols = st.columns(len(examples))
for i, ex in enumerate(examples):
    if cols[i].button(ex):
        st.session_state["query"] = ex

query = st.text_input(
    "Enter search query:",
    value=st.session_state.get("query", ""),
    placeholder="e.g., 'stainless steel screws', '0101', 'electric motors'",
)

k = st.slider("Number of results", 1, 20, 5)

if st.button("🔎 Search"):
    if not query.strip():
        st.error("Please enter a search query.")
    else:
        st.markdown("---")
        st.markdown("### 📄 Results")

        results = semantic_search_hts(query, k)

        for r in results or []:
            st.markdown(
                f"""
                <div style="padding:18px;border-radius:10px;background:#20232a;margin-bottom:14px;border:1px solid #333;">
                    <h3 style="margin:0;color:#e63946;">{r['hts_code']}</h3>
                    <h4 style="margin-top:4px;margin-bottom:10px;color:#fff;">{r['title']}</h4>
                    <details>
                        <summary style="cursor:pointer;">Show Details</summary>
                        <p style="color:#bbb;margin-top:10px;">{r['normalized_text']}</p>
                    </details>
                </div>
                """,
                unsafe_allow_html=True,
            )
