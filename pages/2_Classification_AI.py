import streamlit as st
import textwrap
from utils.llm import classify_hts
from utils.ui import inject_global_css, page_header, result_card
from utils.llm_explain import explain_classification
from utils.duty_rates import get_duty_category

st.set_page_config(
    page_title="Classification AI - HTS Dashboard",
    page_icon="🧠",
    layout="wide",
)

inject_global_css()

page_header(
    "Automated Classification AI",
    "Apply deep semantic logic to complex product specifications. Receive instant HTS alignment with regulatory reasoning."
)

# Example descriptions
st.markdown("### Try An Example")

examples = [
    "Industrial grade PET packaging containers with integrated screw-top sealing mechanisms for high-pressure beverages.",
    "Textile apparel: Men's knitted t-shirts, 100% cotton composition, crew neck construction, short-sleeve traditional fit.",
    "Hardware: M6 Grade 304 stainless steel assembly screws, Phillips drive with low-profile countersunk head.",
    "Construction: Glazed porcelain floor tiles, vitrified body, moisture absorption <0.5%, for high-traffic commercial use.",
    "Industrial: Single-phase asynchronous electric motor, 750W (1.0 HP), NEMA standard frame for heavy-duty applications.",
]

cols = st.columns(len(examples))
for i, ex in enumerate(examples):
    if cols[i].button(f"Example {i+1}", key=f"ex_{i}", use_container_width=True):
        st.session_state["hts_desc"] = ex

st.markdown("<br>", unsafe_allow_html=True)

# Main input area
col1, col2 = st.columns([3, 1])

with col1:
    desc = st.text_area(
        "Product Description",
        value=st.session_state.get("hts_desc", ""),
        placeholder="Describe your product in detail...",
        height=200,
        help="The more detailed your description, the better the AI can classify your product"
    )

with col2:
    st.markdown("### Settings")
    k = st.slider(
        "Number of suggestions",
        min_value=1,
        max_value=10,
        value=5,
    )
    
    show_explanations = st.checkbox(
        "Show AI explanations",
        value=True,
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    classify_button = st.button(
        "Classify Product",
        type="primary",
        use_container_width=True
    )

# Classification logic
if classify_button:
    if not desc.strip():
        st.error("Please enter a product description")
    else:
        with st.spinner("Analyzing product and searching HTS database..."):
            results = classify_hts(desc, k)
        
        if not results:
            st.warning("No results found. Try a different description or broader terms.")
        else:
            st.markdown("---")
            st.markdown(f"## Top {len(results)} Classifications")
            
            # Display results
            for idx, r in enumerate(results):
                similarity = r.get('similarity', 0.85)
                duty_category = get_duty_category(r['hts_code'])
                
                # Render result card from UI library
                result_card(
                    hts_code=r['hts_code'],
                    title=r['title'],
                    description=r.get('normalized_text', 'No additional details available'),
                    similarity=similarity,
                    duty_rate=duty_category,
                )
                
                # AI Explanation section
                if show_explanations:
                    explain_key = f"explain_{idx}_{r['hts_code']}"
                    
                    if explain_key not in st.session_state:
                        st.session_state[explain_key] = None
                    
                    col_a, col_b = st.columns([1, 4])
                    
                    with col_a:
                        if st.button(
                            "Generate Explanation" if not st.session_state[explain_key] else "Regenerate",
                            key=f"btn_{explain_key}",
                            use_container_width=True
                        ):
                            with st.spinner("🧠 Generating explanation..."):
                                explanation = explain_classification(
                                    product_description=desc,
                                    hts_code=r['hts_code'],
                                    hts_title=r['title'],
                                    context=r.get('normalized_text', '')
                                )
                                st.session_state[explain_key] = explanation
                    
                    if st.session_state[explain_key]:
                        st.info(f"**AI Reasoning:**\n\n{st.session_state[explain_key]}")
                
                # Action buttons
                btn1, btn2, btn3 = st.columns(3)
                with btn1:
                    if st.button("📋 Copy Code", key=f"copy_{idx}", use_container_width=True):
                        st.code(r['hts_code'], language=None)
                with btn2:
                    if st.button("View Details", key=f"browser_{idx}", use_container_width=True):
                        st.info(f"HTS Browser link for {r['hts_code']}")
                with btn3:
                    st.button("📊 Analytics", key=f"analytics_{idx}", use_container_width=True, disabled=True)
                
                st.markdown("<br>", unsafe_allow_html=True)

# Sidebar tips
with st.sidebar:
    st.markdown("### Classification Intelligence")
    st.info("""
    **Tips for Best Results:**
    - Be specific about materials
    - Describe the primary use
    - Include technical specs
    - Mention the industry
    """)
    
    st.markdown("---")
    st.markdown("#### Confidence Scores")
    st.markdown("""
    - **90%+** Excellent match
    - **75-89%** Good match
    - **60-74%** Fair match
    """)
    
    st.markdown("---")
    st.markdown("#### Duty Estimates")
    st.markdown("""
    - **Free** 0% duty
    - **Low** 0-5% duty
    - **High** 15%+ duty
    """)
