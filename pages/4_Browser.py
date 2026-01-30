import streamlit as st
from utils.supabase_db import get_hts_page, count_hts_rows

st.title("📚 HTS Browser")
st.write("Browse the HTS schedule page by page.")

total = count_hts_rows()
page_size = 20
total_pages = (total // page_size) + 1

page = st.number_input("Page", 1, total_pages, 1)

rows = get_hts_page(page=page, page_size=page_size)

st.markdown(f"### Showing page {page} of {total_pages}")

for r in rows:
    st.markdown(
        f"""
        <div style="padding:18px;border-radius:10px;background:#1e1e1e;margin-bottom:14px;border:1px solid #333;">
            <h3 style="margin:0;color:#f4a261;">{r['hts_code']}</h3>
            <h4 style="margin-top:4px;margin-bottom:10px;">{r['title']}</h4>
            <details>
                <summary>Show Text</summary>
                <p style="color:#bbb;margin-top:10px;">{r['normalized_text']}</p>
            </details>
        </div>
        """,
        unsafe_allow_html=True,
    )
