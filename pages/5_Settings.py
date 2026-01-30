import os
import streamlit as st

from utils.ui import inject_global_css, page_header, card


inject_global_css()
page_header("⚙️ Settings", "Environment and connection status.")

def check_env(name: str) -> None:
    value = os.environ.get(name)
    if value:
        st.success(f"{name}: ✅ Loaded")
    else:
        st.error(f"{name}: ❌ Missing")


st.markdown("### API & database keys")
check_env("OPENAI_API_KEY")
check_env("SUPABASE_URL")
check_env("SUPABASE_SERVICE_ROLE_KEY")

st.markdown("---")
card(
    "Where are these coming from?",
    "In Streamlit Cloud, these values are stored in **App → Settings → Secrets**.",
    "Locally, they come from your terminal `export` commands or a `.env` file "
    "if you’re loading them with `python-dotenv`.",
)
