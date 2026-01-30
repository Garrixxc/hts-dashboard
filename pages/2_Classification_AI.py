import streamlit as st
from utils.llm import classify_hts

st.title("🧠 HTS Classification Assistant")
st.write("Paste a product description and AI will suggest the most relevant HTS codes.")

st.markdown("### 💡 Example Descriptions:")
examples = [
    "A plastic bottle used for packaging drinking water.",
    "Men’s cotton short-sleeve t-shirt.",
    "Stainless steel screws for furniture assembly.",
]

ex_cols = st.columns(len(examples))
for i, ex in enumerate(ex_cols):
    if ex.button(f"Example {i+1}"):
        st.session_state["hts_desc"] = examples[i]

desc = st.text_area(
    "Product Description:",
    value=st.session_state.get("hts_desc", ""),
    placeholder="Write a detailed product description…",
    height=180,
)

k = st.slider("Number of HTS code suggestions", 1, 10, 3)

if st.button("✨ Classify"):
    if not desc.strip():
        st.error("Please enter a product description.")
    else:
        st.markdown("---")
        st.markdown("### 📦 Suggested Classifications")

        results = classify_hts(desc, k)

        for r in results:
            st.markdown(
                f"""
                <div style="padding:18px;border-radius:10px;background:#1b263b;margin-bottom:14px;border:1px solid #2b3b55;">
                    <h3 style="margin:0;color:#4cc9f0;">{r['hts_code']}</h3>
                    <h4 style="margin:4px 0 10px 0;">{r['title']}</h4>
                    <details>
                        <summary>Show Reference Text</summary>
                        <p style="color:#bbb;margin-top:10px;">{r['normalized_text']}</p>
                    </details>
                </div>
                """,
                unsafe_allow_html=True,
            )
