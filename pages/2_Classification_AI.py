import streamlit as st
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
    "AI Classification Assistant",
    "Describe your product and get instant HTS code suggestions with confidence scores and AI-powered explanations",
    icon="🧠"
)

# Example descriptions
st.markdown('<h3 class="section-title" style="font-size: 20px; margin-top: 24px;">💡 Try an Example</h3>', unsafe_allow_html=True)

examples = [
    "A plastic bottle used for packaging drinking water, made of PET plastic with screw cap",
    "Men's cotton short-sleeve t-shirt, knitted fabric, crew neck, casual wear",
    "Stainless steel screws for furniture assembly, M6 size, Phillips head, corrosion resistant",
    "Ceramic floor tiles, porcelain, glazed finish, 12x12 inches, for residential use",
    "Electric motor, single-phase, 1 horsepower, 1800 RPM, for industrial machinery",
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
        "📝 Product Description",
        value=st.session_state.get("hts_desc", ""),
        placeholder="Describe your product in detail...\n\nInclude:\n• What it's made of (materials)\n• How it's used (purpose/function)\n• Key technical specifications\n• Industry or application\n\nExample: 'Plastic water bottle made of PET, 500ml capacity, with screw cap, used for beverage packaging'",
        height=200,
        help="The more detailed your description, the better the AI can classify your product"
    )

with col2:
    st.markdown("### ⚙️ Settings")
    k = st.slider(
        "Number of suggestions",
        min_value=1,
        max_value=10,
        value=5,
        help="How many HTS code suggestions to show"
    )
    
    show_explanations = st.checkbox(
        "Show AI explanations",
        value=True,
        help="Generate detailed explanations for each classification"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    classify_button = st.button(
        "✨ Classify Product",
        type="primary",
        use_container_width=True
    )

# Classification logic
if classify_button:
    if not desc.strip():
        st.error("⚠️ Please enter a product description")
    else:
        with st.spinner("🔍 Analyzing product and searching HTS database..."):
            results = classify_hts(desc, k)
        
        if not results:
            st.warning("No results found. Try a different description or broader terms.")
        else:
            st.markdown("---")
            st.markdown(f'<h2 class="section-title">📦 Top {len(results)} Classifications</h2>', unsafe_allow_html=True)
            st.markdown(
                f'<p class="subtitle">Found {len(results)} potential matches. Review confidence scores and explanations below.</p>',
                unsafe_allow_html=True
            )
            
            # Display results
            for idx, r in enumerate(results):
                # Calculate similarity score (assuming it's in the result)
                similarity = r.get('similarity', 0.85)  # Default if not provided
                
                # Get duty category
                duty_category = get_duty_category(r['hts_code'])
                
                # Create expandable section for each result
                with st.expander(
                    f"#{idx+1}: {r['hts_code']} - {r['title'][:80]}{'...' if len(r['title']) > 80 else ''}",
                    expanded=(idx == 0)  # Expand first result by default
                ):
                    # Result card with all details
                    result_card(
                        hts_code=r['hts_code'],
                        title=r['title'],
                        description=r.get('normalized_text', 'No additional details available'),
                        similarity=similarity,
                        duty_rate=duty_category,
                        show_explain=False  # We'll handle explanation separately
                    )
                    
                    # AI Explanation section
                    if show_explanations:
                        st.markdown("---")
                        st.markdown("### 🤖 AI Explanation")
                        
                        # Generate explanation button
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
                        
                        # Display explanation if generated
                        if st.session_state[explain_key]:
                            st.markdown(
                                f"""
                                <div class="glass-card" style="margin-top: 16px;">
                                    {st.session_state[explain_key]}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    
                    # Action buttons
                    st.markdown("<br>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("📋 Copy Code", key=f"copy_{idx}", use_container_width=True):
                            st.code(r['hts_code'], language=None)
                            st.success("Code displayed above!")
                    
                    with col2:
                        if st.button("🔍 View in Browser", key=f"browser_{idx}", use_container_width=True):
                            st.info(f"Navigate to HTS Browser and search for: {r['hts_code']}")
                    
                    with col3:
                        if st.button("📊 See Analytics", key=f"analytics_{idx}", use_container_width=True):
                            st.info("Analytics feature coming soon!")

# Sidebar tips
with st.sidebar:
    st.markdown("### 💡 Classification Tips")
    
    st.markdown(
        """
        <div class="glass-card">
            <h4 style="color: var(--accent-blue); margin-bottom: 12px;">For Best Results:</h4>
            <ul style="font-size: 14px; line-height: 1.8; color: rgba(255, 255, 255, 0.8);">
                <li><strong>Be specific</strong> about materials</li>
                <li><strong>Describe</strong> the primary use</li>
                <li><strong>Include</strong> technical specs</li>
                <li><strong>Mention</strong> the industry</li>
                <li><strong>Avoid</strong> brand names</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="glass-card">
            <h4 style="color: var(--accent-purple); margin-bottom: 12px;">Understanding Scores:</h4>
            <ul style="font-size: 13px; line-height: 1.8; color: rgba(255, 255, 255, 0.8);">
                <li><span class="badge-success" style="padding: 2px 8px; border-radius: 4px;">90%+</span> Excellent match</li>
                <li><span class="badge-info" style="padding: 2px 8px; border-radius: 4px;">75-89%</span> Good match</li>
                <li><span class="badge-warning" style="padding: 2px 8px; border-radius: 4px;">60-74%</span> Fair match</li>
                <li><span class="badge-error" style="padding: 2px 8px; border-radius: 4px;">&lt;60%</span> Weak match</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="glass-card">
            <h4 style="color: var(--accent-pink); margin-bottom: 12px;">Duty Categories:</h4>
            <ul style="font-size: 13px; line-height: 1.8; color: rgba(255, 255, 255, 0.8);">
                <li><span class="duty-free" style="padding: 2px 8px; border-radius: 4px;">Free</span> 0% duty</li>
                <li><span class="duty-low" style="padding: 2px 8px; border-radius: 4px;">Low</span> 0-5% duty</li>
                <li><span class="duty-medium" style="padding: 2px 8px; border-radius: 4px;">Medium</span> 5-15% duty</li>
                <li><span class="duty-high" style="padding: 2px 8px; border-radius: 4px;">High</span> 15%+ duty</li>
            </ul>
            <p style="font-size: 11px; color: rgba(255, 255, 255, 0.5); margin-top: 12px;">
                ⚠️ Estimates only. Verify with official sources.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
