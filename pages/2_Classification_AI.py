import streamlit as st
import textwrap
from utils.llm import classify_hts
from utils.ui import inject_global_css, page_header
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
    "Apply deep semantic logic to complex product specifications. Receive instant HTS alignment with regulatory reasoning and confidence metrics.",
    icon="🛡️"
)

# Example descriptions
st.markdown('<h3 class="section-title" style="font-size: 20px; margin-top: 24px;">💡 Try an Example</h3>', unsafe_allow_html=True)

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
                # Calculate similarity score
                similarity = r.get('similarity', 0.85)
                
                # Get duty category
                duty_category = get_duty_category(r['hts_code'])
                
                # Build confidence badge HTML
                percentage = int(similarity * 100)
                if percentage >= 90:
                    badge_class = "confidence-high"
                    icon = "✓"
                    label = "Excellent Match"
                elif percentage >= 75:
                    badge_class = "confidence-medium"
                    icon = "~"
                    label = "Good Match"
                elif percentage >= 60:
                    badge_class = "confidence-low"
                    icon = "!"
                    label = "Fair Match"
                else:
                    badge_class = "confidence-very-low"
                    icon = "?"
                    label = "Weak Match"
                
                confidence_html = textwrap.dedent(f'''
                    <div class="confidence-badge {badge_class}">
                        <span style="font-size: 16px;">{icon}</span>
                        <span>{percentage}% - {label}</span>
                    </div>
                ''').strip()
                
                # Build similarity bar HTML
                similarity_html = textwrap.dedent(f'''
                    <div class="similarity-bar">
                        <div class="similarity-fill" style="width: {percentage}%;"></div>
                    </div>
                ''').strip()
                
                # Build duty tag HTML
                duty_classes = {
                    "Free": "duty-free",
                    "Low": "duty-low",
                    "Medium": "duty-medium",
                    "High": "duty-high",
                }
                duty_class = duty_classes.get(duty_category, "duty-medium")
                duty_html = f'<span class="duty-tag {duty_class}">{duty_category} Duty</span>'
                
                # Render the result card
                result_html = textwrap.dedent(f'''
                <div class="result-card">
                    <div class="result-header">
                        <div>
                            <div class="hts-code">{r['hts_code']}</div>
                            <div class="hts-title">{r['title']}</div>
                            <div style="margin-top: 8px;">{duty_html}</div>
                        </div>
                        <div>
                            {confidence_html}
                        </div>
                    </div>
                    {similarity_html}
                    <details style="margin-top: 16px;">
                        <summary style="cursor: pointer; color: rgba(255, 255, 255, 0.7); font-size: 14px;">
                            Show full description
                        </summary>
                        <div class="hts-description">{r.get('normalized_text', 'No additional details available')}</div>
                    </details>
                </div>
                ''').strip()
                
                st.markdown(result_html, unsafe_allow_html=True)
                
                # AI Explanation section (outside the main card)
                if show_explanations:
                    explain_key = f"explain_{idx}_{r['hts_code']}"
                    
                    if explain_key not in st.session_state:
                        st.session_state[explain_key] = None
                    
                    col_a, col_b = st.columns([1, 4])
                    
                    with col_a:
                        if st.button(
                            "🤖 Generate Explanation" if not st.session_state[explain_key] else "🔄 Regenerate",
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
                        explanation_html = textwrap.dedent(f'''
                        <div class="glass-card" style="margin-top: 16px; margin-bottom: 24px;">
                            <h4 style="color: var(--accent-blue); margin-bottom: 12px;">🤖 AI Explanation</h4>
                            <div style="font-size: 14px; line-height: 1.6;">
                                {st.session_state[explain_key]}
                            </div>
                        </div>
                        ''').strip()
                        st.markdown(explanation_html, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📋 Copy Code", key=f"copy_{idx}", use_container_width=True):
                        st.code(r['hts_code'], language=None)
                        st.success("Code displayed!")
                
                with col2:
                    if st.button("🔍 View in Browser", key=f"browser_{idx}", use_container_width=True):
                        st.info(f"Search for {r['hts_code']} in the Browser page")
                
                with col3:
                    if st.button("📊 See Analytics", key=f"analytics_{idx}", use_container_width=True):
                        st.info("Analytics coming soon!")
                
                st.markdown("<br>", unsafe_allow_html=True)

# Sidebar tips
with st.sidebar:
    st.markdown("### 💡 Classification Tips")
    
    st.markdown(
        textwrap.dedent("""
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
        """),
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(
        textwrap.dedent("""
        <div class="glass-card">
            <h4 style="color: var(--accent-purple); margin-bottom: 12px;">Understanding Scores:</h4>
            <ul style="font-size: 13px; line-height: 1.8; color: rgba(255, 255, 255, 0.8);">
                <li><span class="badge-success" style="padding: 2px 8px; border-radius: 4px;">90%+</span> Excellent match</li>
                <li><span class="badge-info" style="padding: 2px 8px; border-radius: 4px;">75-89%</span> Good match</li>
                <li><span class="badge-warning" style="padding: 2px 8px; border-radius: 4px;">60-74%</span> Fair match</li>
                <li><span class="badge-error" style="padding: 2px 8px; border-radius: 4px;">&lt;60%</span> Weak match</li>
            </ul>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(
        textwrap.dedent("""
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
        """),
        unsafe_allow_html=True
    )
