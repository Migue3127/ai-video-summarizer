import streamlit as st
from src.translations import get_translation
import time

def tutorial_page():
    # Configuração de estilo avançada
    st.markdown("""
    <style>
        .tutorial-container {
            max-width: 900px;
            margin: 0 auto;
        }
        .tutorial-header {
            background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
        }
        .tutorial-step {
            background-color: #f8fafc;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-left: 4px solid #4f46e5;
            transition: all 0.3s ease;
        }
        .tutorial-step:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .tutorial-step-number {
            display: inline-block;
            background-color: #4f46e5;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            text-align: center;
            line-height: 30px;
            margin-right: 10px;
            font-weight: bold;
        }
        .tutorial-video-container {
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            margin: 1.5rem 0;
            border-radius: 12px;
        }
        .tutorial-video-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
        .tutorial-tip {
            background-color: #e0e7ff;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 4px solid #818cf8;
        }
        .tutorial-feature-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }
        .tutorial-badge {
            display: inline-block;
            background-color: #4f46e5;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
        .tutorial-pro-tip {
            background-color: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-left: 4px solid #22c55e;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Container principal
    with st.container():
        # Header
        st.markdown(f"""
        <div class="tutorial-header">
            <h1 style="margin:0">📚 {get_translation(st.session_state.lang, "tutorial_title")}</h1>
            <p style="margin:0; opacity:0.9">{get_translation(st.session_state.lang, "tutorial_subtitle")}</p>
        </div>
        """, unsafe_allow_html=True)

        # Seção de introdução
        with st.container():
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.markdown('<div class="tutorial-step-number">!</div>', unsafe_allow_html=True)
            with col2:
                st.header(get_translation(st.session_state.lang, "introduction"))
            
            st.write(get_translation(st.session_state.lang, "tutorial_intro_text"))
            
            with st.expander(f"💡 {get_translation(st.session_state.lang, 'ideal_for')}"):
                st.write(get_translation(st.session_state.lang, "ideal_for_description"))
            
        
        # Passo 1 - Inserção de URL
        with st.container():
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.markdown('<div class="tutorial-step-number">1</div>', unsafe_allow_html=True)
            with col2:
                st.header(get_translation(st.session_state.lang, "url_label"))
            
            st.write(get_translation(st.session_state.lang, "step1_text"))
            
            with st.container():
                st.subheader(f"📌 {get_translation(st.session_state.lang, 'supported_formats')}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f'<span class="tutorial-badge">{get_translation(st.session_state.lang, "standard_format")}</span>', unsafe_allow_html=True)
                    st.code("https://www.youtube.com/watch?v=VIDEO_ID")
                with col2:
                    st.markdown(f'<span class="tutorial-badge">{get_translation(st.session_state.lang, "short_format")}</span>', unsafe_allow_html=True)
                    st.code("https://youtube.com/shorts/VIDEO_ID")
                with col3:
                    st.markdown(f'<span class="tutorial-badge">{get_translation(st.session_state.lang, "embed_format")}</span>', unsafe_allow_html=True)
                    st.code("https://youtu.be/VIDEO_ID")
                
                with st.expander(f"✨ {get_translation(st.session_state.lang, 'pro_tip')}"):
                    st.write(get_translation(st.session_state.lang, "drag_drop_tip"))
        
        # Passo 2 - Configurações
        with st.container():
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.markdown('<div class="tutorial-step-number">2</div>', unsafe_allow_html=True)
            with col2:
                st.header(get_translation(st.session_state.lang, "customize_summary"))
            
            st.write(get_translation(st.session_state.lang, "step2_text"))
            
            with st.container():
                st.subheader(f"🌐 {get_translation(st.session_state.lang, 'output_language')}")
                st.write(get_translation(st.session_state.lang, "choose_language_text"))
                cols = st.columns(5)
                with cols[0]:
                    st.markdown('<span class="tutorial-badge">🇵🇹 Português</span>', unsafe_allow_html=True)
                with cols[1]:
                    st.markdown('<span class="tutorial-badge">🇬🇧 English</span>', unsafe_allow_html=True)
                with cols[2]:
                    st.markdown('<span class="tutorial-badge">🇪🇸 Español</span>', unsafe_allow_html=True)
                with cols[3]:
                    st.markdown('<span class="tutorial-badge">🇫🇷 Français</span>', unsafe_allow_html=True)
                with cols[4]:
                    st.markdown('<span class="tutorial-badge">🇩🇪 Deutsch</span>', unsafe_allow_html=True)
            
            with st.container():
                st.subheader(f"📏 {get_translation(st.session_state.lang, 'detail_level')}")
                st.write(get_translation(st.session_state.lang, "choose_detail_text"))
                st.markdown(f"- **{get_translation(st.session_state.lang, 'quick')}** - {get_translation(st.session_state.lang, 'quick_description')}")
                st.markdown(f"- **{get_translation(st.session_state.lang, 'standard')}** - {get_translation(st.session_state.lang, 'standard_description')}")
                st.markdown(f"- **{get_translation(st.session_state.lang, 'premium')}** - {get_translation(st.session_state.lang, 'premium_description')}")
                
                with st.expander(f"⚡ {get_translation(st.session_state.lang, 'speed_vs_detail')}"):
                    st.write(get_translation(st.session_state.lang, "speed_detail_tip"))
        
        # Passo 3 - Geração do resumo
        with st.container():
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.markdown('<div class="tutorial-step-number">3</div>', unsafe_allow_html=True)
            with col2:
                st.header(get_translation(st.session_state.lang, "generate_summary"))
            
            st.write(get_translation(st.session_state.lang, "step3_text"))
            
            with st.container():
                st.subheader(f"⏱️ {get_translation(st.session_state.lang, 'processing_time')}")
                st.write(get_translation(st.session_state.lang, "processing_time_text"))
                st.markdown(f"- {get_translation(st.session_state.lang, 'short_videos')}")
                st.markdown(f"- {get_translation(st.session_state.lang, 'medium_videos')}")
                st.markdown(f"- {get_translation(st.session_state.lang, 'long_videos')}")
                
                with st.expander(f"🔍 {get_translation(st.session_state.lang, 'technology')}"):
                    st.write(get_translation(st.session_state.lang, "tech_description"))
            
            with st.expander(f"📊 {get_translation(st.session_state.lang, 'analyzed_data')}"):
                st.write(get_translation(st.session_state.lang, "data_analysis_text"))
        
        # Passo 4 - Explorando resultados
        with st.container():
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.markdown('<div class="tutorial-step-number">4</div>', unsafe_allow_html=True)
            with col2:
                st.header(get_translation(st.session_state.lang, "explore_results"))
            
            st.write(get_translation(st.session_state.lang, "step4_text"))
            
            tabs = st.tabs([
                f"📖 {get_translation(st.session_state.lang, 'summary_tab')}",
                f"⏱️ {get_translation(st.session_state.lang, 'timestamps_tab')}",
                f"📜 {get_translation(st.session_state.lang, 'transcript_tab')}"
            ])
            
            with tabs[0]:
                st.write(get_translation(st.session_state.lang, "summary_features"))
                st.markdown(f"- {get_translation(st.session_state.lang, 'descriptive_title')}")
                st.markdown(f"- {get_translation(st.session_state.lang, 'content_overview')}")
                st.markdown(f"- {get_translation(st.session_state.lang, 'key_points')}")
                st.markdown(f"- {get_translation(st.session_state.lang, 'main_conclusions')}")
                st.markdown(f"- {get_translation(st.session_state.lang, 'additional_context')}")
            
            with tabs[1]:
                st.write(get_translation(st.session_state.lang, "timeline_features"))
                st.markdown(f"- {get_translation(st.session_state.lang, 'clickable_timestamps')}")
                st.markdown(f"- {get_translation(st.session_state.lang, 'organized_topics')}")
                st.markdown(f"- {get_translation(st.session_state.lang, 'direct_links')}")
                st.markdown(f"- {get_translation(st.session_state.lang, 'relevant_moments')}")
            
            with tabs[2]:
                st.write(get_translation(st.session_state.lang, "transcript_features"))
                st.markdown(f"- {get_translation(st.session_state.lang, 'original_text')}")
                st.markdown(f"- {get_translation(st.session_state.lang, 'auto_translation')}")
                st.markdown(f"- {get_translation(st.session_state.lang, 'bilingual_mode')}")
                st.markdown(f"- {get_translation(st.session_state.lang, 'technical_terms')}")
        
        # Passo 5 - Recursos avançados
        with st.container():
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.markdown('<div class="tutorial-step-number">5</div>', unsafe_allow_html=True)
            with col2:
                st.header(get_translation(st.session_state.lang, "advanced_features"))
            
            cols = st.columns(2)
            
            with cols[0]:
                with st.container():
                    st.subheader(f"🔊 {get_translation(st.session_state.lang, 'tts_title')}")
                    st.write(get_translation(st.session_state.lang, "tts_features"))
                    st.markdown(f"- {get_translation(st.session_state.lang, 'native_voices')}")
                    st.markdown(f"- {get_translation(st.session_state.lang, 'speed_control')}")
                    st.markdown(f"- {get_translation(st.session_state.lang, 'mp3_download')}")
                    st.markdown(f"- {get_translation(st.session_state.lang, 'auto_playback')}")
            
            with cols[1]:
                with st.container():
                    st.subheader(f"📚 {get_translation(st.session_state.lang, 'history')}")
                    st.write(get_translation(st.session_state.lang, "history_features"))
                    st.markdown(f"- {get_translation(st.session_state.lang, 'last_10_summaries')}")
                    st.markdown(f"- {get_translation(st.session_state.lang, 'individual_deletion')}")
                    st.markdown(f"- {get_translation(st.session_state.lang, 'smart_cache')}")
                    
                    with st.expander(f"🔒 {get_translation(st.session_state.lang, 'security')}"):
                        st.write(get_translation(st.session_state.lang, "security_description"))
            
            with st.container():
                st.subheader(f"📤 {get_translation(st.session_state.lang, 'export')}")
                st.write(get_translation(st.session_state.lang, "export_features"))
                st.markdown(f"- {get_translation(st.session_state.lang, 'copy_clipboard')}")
                st.markdown(f"- {get_translation(st.session_state.lang, 'download_txt')}")
        
        # Seção final
        st.markdown("---")
        st.subheader(f"🎉 {get_translation(st.session_state.lang, 'ready_to_start')}")
        st.write(get_translation(st.session_state.lang, "final_tutorial_text"))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🏠 {get_translation(st.session_state.lang, 'back_to_home')}", 
                        key="tutorial_back_home", use_container_width=True):
                st.session_state.current_page = 'main'
                st.rerun()
        with col2:
            if st.button(f"🚀 {get_translation(st.session_state.lang, 'why_use_videomind')}", 
                        key="tutorial_why_use", use_container_width=True):
                st.session_state.current_page = 'why_use'
                st.rerun()