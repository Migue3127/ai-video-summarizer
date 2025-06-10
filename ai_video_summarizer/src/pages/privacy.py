import streamlit as st
from src.translations import get_translation

def privacy_page():
    st.markdown("""
    <style>
        .privacy-section { margin-bottom: 2rem; }
        .privacy-header { color: #4f46e5; margin-bottom: 1rem; }
        .privacy-subheader { color: #64748b; font-weight: 500; margin-bottom: 1.5rem; }
        .privacy-item { margin-bottom: 1.5rem; padding-left: 1rem; border-left: 3px solid #e2e8f0; }
        .privacy-highlight {
            background-color: #f1f5fe;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1.5rem 0;
        }
        .privacy-contact {
            background-color: #f8fafc;
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title(f"🔐 {get_translation(st.session_state.lang, 'privacy_title')}")
    st.caption(f"{get_translation(st.session_state.lang, 'last_update')}: 15/05/2025")

    st.markdown(get_translation(st.session_state.lang, "privacy_intro"))

    st.markdown(f"""
    <div class="privacy-highlight">
        <strong>⚠️ {get_translation(st.session_state.lang, 'important_note')}:</strong> {get_translation(st.session_state.lang, 'privacy_project_note')}
    </div>
    """, unsafe_allow_html=True)

    # Section 1
    st.header(f"1. {get_translation(st.session_state.lang, 'privacy_section1')}")
    st.markdown(f"""
    - **{get_translation(st.session_state.lang, 'account_data')}**: {get_translation(st.session_state.lang, 'account_data_desc')}
    - **{get_translation(st.session_state.lang, 'preferences')}**: {get_translation(st.session_state.lang, 'preferences_desc')}
    - **{get_translation(st.session_state.lang, 'usage_history')}**: {get_translation(st.session_state.lang, 'usage_history_desc')}
    
    ❌ {get_translation(st.session_state.lang, 'data_not_collected')}
    """)

    # Section 2
    st.header(f"2. {get_translation(st.session_state.lang, 'privacy_section2')}")
    st.markdown(f"""
    {get_translation(st.session_state.lang, 'data_usage_desc')}
    
    - {get_translation(st.session_state.lang, 'process_videos')}
    - {get_translation(st.session_state.lang, 'save_history')}
    - {get_translation(st.session_state.lang, 'improve_usability')}

    🚫 {get_translation(st.session_state.lang, 'data_not_used_for')}
    """)

    # Section 3
    st.header(f"3. {get_translation(st.session_state.lang, 'privacy_section3')}")
    st.markdown(f"""
    - {get_translation(st.session_state.lang, 'data_storage_desc1')}
    - {get_translation(st.session_state.lang, 'data_storage_desc2')}

    🛡️ **{get_translation(st.session_state.lang, 'security')}:**
    - {get_translation(st.session_state.lang, 'passwords_protected')}
    - {get_translation(st.session_state.lang, 'cache_expires')}
    
    🗑️ **{get_translation(st.session_state.lang, 'delete_data')}:**
    - {get_translation(st.session_state.lang, 'delete_individual')}
    - {get_translation(st.session_state.lang, 'delete_completely')}
    """)

    # Section 4
    st.header(f"4. {get_translation(st.session_state.lang, 'privacy_section4')}")
    st.markdown(f"""
    {get_translation(st.session_state.lang, 'legal_compliance_intro')}

    - {get_translation(st.session_state.lang, 'gdpr_compliance')}
    - {get_translation(st.session_state.lang, 'youtube_api_policy')}
    - {get_translation(st.session_state.lang, 'gemini_api_rules')}

    ⚠️ **{get_translation(st.session_state.lang, 'limitations')}:**
    - {get_translation(st.session_state.lang, 'no_private_videos')}
    - {get_translation(st.session_state.lang, 'personal_use_only')}
    - {get_translation(st.session_state.lang, 'no_copyright_violation')}
    """)

    # Section 5
    st.header(f"5. {get_translation(st.session_state.lang, 'privacy_section5')}")
    st.markdown(f"""
    {get_translation(st.session_state.lang, 'user_responsibilities_intro')}

    - {get_translation(st.session_state.lang, 'authorized_content_only')}
    - {get_translation(st.session_state.lang, 'secure_credentials')}
    - {get_translation(st.session_state.lang, 'no_illegal_use')}
    """)

    st.markdown("---")
    st.caption(get_translation(st.session_state.lang, "academic_project_footer"))