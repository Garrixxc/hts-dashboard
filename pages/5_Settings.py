import os
import sys
import streamlit as st
import textwrap
from utils.ui import inject_global_css, page_header, glass_card

st.set_page_config(
    page_title="Settings - HTS Dashboard",
    page_icon="⚙️",
    layout="wide",
)

inject_global_css()

page_header(
    "Compliance Configuration",
    "Manage environment variables, secure API gateways, and global system health metrics."
)

def check_env(name: str) -> tuple[bool, str]:
    """Check if environment variable is set and return status."""
    value = os.environ.get(name)
    if value:
        masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
        return True, masked
    return False, "Not set"

st.markdown("### API & Database Configuration")

# Check each environment variable
env_vars = [
    ("OPENAI_API_KEY", "OpenAI API", "Required for embeddings and LLM explanations"),
    ("SUPABASE_URL", "Supabase URL", "Database connection endpoint"),
    ("SUPABASE_SERVICE_ROLE_KEY", "Supabase Key", "Database authentication"),
    ("EMBEDDING_MODEL", "Embedding Model", "OpenAI embedding model name"),
    ("EMBEDDING_DIM", "Embedding Dimension", "Vector dimension (usually 1536)"),
]

for var_name, display_name, description in env_vars:
    is_set, value = check_env(var_name)
    
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{display_name}**")
            st.caption(description)
            st.code(var_name)
        with col2:
            if is_set:
                st.success("Configured")
            else:
                st.error("Missing")
        st.markdown("---")

# Configuration info
st.markdown("### Configuration Guide")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    #### ☁️ Streamlit Cloud
    In Streamlit Cloud, these values are stored in:
    1. Go to your app dashboard
    2. Click **Settings**
    3. Navigate to **Secrets**
    4. Add your environment variables in TOML format
    """)

with col2:
    st.info("""
    #### 💻 Local Development
    For local development, you can:
    1. Export variables in your terminal
    2. Use a `.env` file with `python-dotenv`
    3. Set them in your IDE configuration
    """)

# System info
st.markdown("### System Information")

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Python", sys.version.split()[0])
with c2: st.metric("Streamlit", st.__version__)
with c3: st.metric("Platform", sys.platform)
with c4: st.metric("Environment", "Cloud" if os.environ.get("STREAMLIT_SHARING_MODE") else "Local")

# Sidebar
with st.sidebar:
    st.markdown("### Security Note")
    st.warning("""
    **Important Safety Guidelines:**
    - Never commit API keys to Git
    - Use environment variables
    - Rotate keys regularly
    - Monitor API usage
    """)
