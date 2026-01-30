import streamlit as st
from datetime import datetime

def log_search(query, results):
    if "history" not in st.session_state:
        st.session_state["history"] = []

    st.session_state["history"].append({
        "time": datetime.utcnow().isoformat(timespec="seconds"),
        "query": query,
        "top_results": ", ".join(r.get("hts_code") for r in results),
    })
