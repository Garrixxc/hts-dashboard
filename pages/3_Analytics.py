import streamlit as st

from utils.ui import inject_global_css, page_header, card
# from utils.analytics import get_usage_metrics  # 🔁 optional future hook


inject_global_css()
page_header("📊 Analytics", "High-level view of how you use the HTS tools.")

st.markdown("### Usage overview")

# 🔁 If you later implement logging, replace this whole block with real metrics.
card(
    "No search history yet",
    "You haven't wired up analytics logging to Supabase yet, "
    "so there’s nothing to chart here.",
    "When you're ready, store each search in a `search_logs` table and surface "
    "those metrics here (e.g., most common queries, error rate, etc.).",
)

st.markdown("---")
st.caption(
    "Ideas: track search count per day, top queries, zero-result queries, "
    "and the distribution of chapters used."
)
