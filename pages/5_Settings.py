import os
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
    "Settings & Configuration",
    "Environment status, API connections, and system configuration",
    icon="⚙️"
)

def check_env(name: str) -> tuple[bool, str]:
    """Check if environment variable is set and return status."""
    value = os.environ.get(name)
    if value:
        # Mask the value for security
        masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
        return True, masked
    return False, "Not set"

st.markdown('<h3 class="section-title" style="font-size: 20px; margin-top: 24px;">🔑 API & Database Keys</h3>', unsafe_allow_html=True)

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
    
    if is_set:
        badge_class = "badge-success"
        icon = "✅"
        status = "Configured"
    else:
        badge_class = "badge-error"
        icon = "❌"
        status = "Missing"
    
    content = textwrap.dedent(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 16px;">
            <div>
                <h4 style="margin: 0; color: #fff; font-size: 16px;">{display_name}</h4>
                <p style="margin: 4px 0 0 0; font-size: 13px; color: rgba(255, 255, 255, 0.6);">
                    {description}
                </p>
                <code style="font-size: 12px; color: rgba(255, 255, 255, 0.5); margin-top: 4px; display: block;">
                    {var_name}
                </code>
            </div>
            <div>
                <span class="badge {badge_class}">
                    {icon} {status}
                </span>
            </div>
        </div>
    """).strip()
    
    glass_card(content, premium=False)

st.markdown("<br>", unsafe_allow_html=True)

# Configuration info
st.markdown('<h3 class="section-title" style="font-size: 20px;">📝 Configuration Guide</h3>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    streamlit_cloud = textwrap.dedent("""
    <div style="padding: 20px;">
        <h4 style="color: var(--accent-blue); margin-bottom: 16px;">☁️ Streamlit Cloud</h4>
        <p style="font-size: 14px; line-height: 1.6; color: rgba(255, 255, 255, 0.8);">
            In Streamlit Cloud, these values are stored in:
        </p>
        <ol style="font-size: 13px; line-height: 1.8; color: rgba(255, 255, 255, 0.7); margin-top: 12px;">
            <li>Go to your app dashboard</li>
            <li>Click <strong>Settings</strong></li>
            <li>Navigate to <strong>Secrets</strong></li>
            <li>Add your environment variables in TOML format</li>
        </ol>
        <br>
        <p style="font-size: 12px; color: rgba(255, 255, 255, 0.5);">
            Example format:<br>
            <code>OPENAI_API_KEY = "sk-..."</code>
        </p>
    </div>
    """).strip()
    glass_card(streamlit_cloud, premium=False)

with col2:
    local_dev = textwrap.dedent("""
    <div style="padding: 20px;">
        <h4 style="color: var(--accent-purple); margin-bottom: 16px;">💻 Local Development</h4>
        <p style="font-size: 14px; line-height: 1.6; color: rgba(255, 255, 255, 0.8);">
            For local development, you can:
        </p>
        <ol style="font-size: 13px; line-height: 1.8; color: rgba(255, 255, 255, 0.7); margin-top: 12px;">
            <li>Export variables in your terminal</li>
            <li>Use a <code>.env</code> file with python-dotenv</li>
            <li>Set them in your IDE configuration</li>
        </ol>
        <br>
        <p style="font-size: 12px; color: rgba(255, 255, 255, 0.5);">
            Example:<br>
            <code>export OPENAI_API_KEY="sk-..."</code>
        </p>
    </div>
    """).strip()
    glass_card(local_dev, premium=False)

st.markdown("<br>", unsafe_allow_html=True)

# System info
st.markdown('<h3 class="section-title" style="font-size: 20px;">ℹ️ System Information</h3>', unsafe_allow_html=True)

import sys
import streamlit as st_version

system_info = textwrap.dedent(f"""
<div style="padding: 20px;">
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;">
        <div>
            <p style="font-size: 13px; color: rgba(255, 255, 255, 0.6);">Python Version</p>
            <p style="font-size: 16px; color: #fff; font-weight: 600;">{sys.version.split()[0]}</p>
        </div>
        <div>
            <p style="font-size: 13px; color: rgba(255, 255, 255, 0.6);">Streamlit Version</p>
            <p style="font-size: 16px; color: #fff; font-weight: 600;">{st_version.__version__}</p>
        </div>
        <div>
            <p style="font-size: 13px; color: rgba(255, 255, 255, 0.6);">Platform</p>
            <p style="font-size: 16px; color: #fff; font-weight: 600;">{sys.platform}</p>
        </div>
        <div>
            <p style="font-size: 13px; color: rgba(255, 255, 255, 0.6);">Environment</p>
            <p style="font-size: 16px; color: #fff; font-weight: 600;">
                {"Streamlit Cloud" if os.environ.get("STREAMLIT_SHARING_MODE") else "Local"}
            </p>
        </div>
    </div>
</div>
""").strip()

glass_card(system_info, premium=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🔒 Security Note")
    
    security = textwrap.dedent("""
    <div class="glass-card">
        <p style="font-size: 13px; line-height: 1.6; color: rgba(255, 255, 255, 0.8);">
            <strong>⚠️ Important:</strong>
        </p>
        <ul style="font-size: 12px; line-height: 1.8; color: rgba(255, 255, 255, 0.7); margin-top: 8px;">
            <li>Never commit API keys to Git</li>
            <li>Use environment variables</li>
            <li>Rotate keys regularly</li>
            <li>Monitor API usage</li>
            <li>Use service role keys carefully</li>
        </ul>
    </div>
    """).strip()
    st.markdown(security, unsafe_allow_html=True)
