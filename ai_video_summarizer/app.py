import streamlit as st
import re
import sqlite3
from datetime import datetime
import hashlib
import time
from src.video_info import GetVideo
from src.model import Model
from src.prompt import Prompt
from src.misc import Misc
from src.translations import get_translation, language_options
from src.action_buttons import create_action_buttons
from dotenv import load_dotenv
import streamlit.components.v1 as components
from src.tts import TextToSpeech
from src.pages import tutorial as tutorial_page
from src.pages import why_use as why_use_page
from src.pages import faq as faq_page
from src.pages import privacy as privacy_page

# =============================================
# CONFIGURAÇÃO INICIAL
# =============================================
st.set_page_config(
    page_title="VideoMind PRO",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)
load_dotenv()

# =============================================
# BANCO DE DADOS (CACHE + HISTÓRICO + UTILIZADORES)
# =============================================
def init_db():
    from src.database import init_db
    init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    conn = sqlite3.connect('resumos.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ? AND password = ?", 
             (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

def register_user(username, password):
    try:
        conn = sqlite3.connect('resumos.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                 (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def save_history(user_id, video_url, video_title, summary, language, detail_level):
    conn = sqlite3.connect('resumos.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("""INSERT INTO history 
                 (user_id, video_url, video_title, summary, language, detail_level, created_at) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
             (user_id, video_url, video_title, summary, language, detail_level, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def remove_from_history(user_id, video_url):
    conn = sqlite3.connect('resumos.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM history WHERE user_id = ? AND video_url = ?", 
             (user_id, video_url))
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = sqlite3.connect('resumos.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("""
        SELECT video_url, video_title, summary, language, detail_level, created_at 
        FROM history 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT 10
    """, (user_id,))
    history = c.fetchall()
    conn.close()
    return history

def get_cached_summary(user_id, video_id, language, detail_level):
    conn = sqlite3.connect('resumos.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("""SELECT summary FROM cache 
                 WHERE user_id=? AND video_id=? AND language=? AND detail_level=?
                 AND (expires_at IS NULL OR expires_at > datetime('now'))""", 
             (user_id, video_id, language, detail_level))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def save_to_cache(user_id, video_id, summary, language, detail_level):
    conn = sqlite3.connect('resumos.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("""INSERT INTO cache 
                 (user_id, video_id, summary, language, detail_level, created_at, expires_at) 
                 VALUES (?, ?, ?, ?, ?, ?, datetime('now', '+7 days'))""",
              (user_id, video_id, summary, language, detail_level, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

# =============================================
# CLASSE PRINCIPAL
# =============================================
class AIVideoSummarizer:
    def __init__(self):
        init_db()
        st.session_state.setdefault('lang', 'pt')
        st.session_state.setdefault('youtube_url', '')
        st.session_state.setdefault('current_page', 'main')
        
        # Mapeamento de idiomas
        self.output_language_options = {
            'pt': {'Português': 'pt', 'Inglês': 'en', 'Espanhol': 'es', 'Francês': 'fr', 'Alemão': 'de'},
            'en': {'Portuguese': 'pt', 'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de'},
            'es': {'Portugués': 'pt', 'Inglés': 'en', 'Español': 'es', 'Francés': 'fr', 'Alemán': 'de'},
            'fr': {'Portugais': 'pt', 'Anglais': 'en', 'Espagnol': 'es', 'Français': 'fr', 'Allemand': 'de'},
            'de': {'Portugiesisch': 'pt', 'Englisch': 'en', 'Spanisch': 'es', 'Französisch': 'fr', 'Deutsch': 'de'}
        }
        
        self.setup_ui()

    def _embed_video_preview(self, video_id):
        try:
            st.markdown(f"""
            <style>
                .responsive-video-container {{
                    position: relative;
                    padding-bottom: 56.25%;
                    height: 0;
                    overflow: hidden;
                    margin-bottom: 1rem;
                    border-radius: 12px;
                }}
                .responsive-video-container iframe {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    border: none;
                }}
            </style>
            <div class="responsive-video-container">
                <iframe src="https://www.youtube.com/embed/{video_id}?modestbranding=1&rel=0" 
                        frameborder="0" allowfullscreen>
                </iframe>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.warning(get_translation(st.session_state.lang, "video_preview_error"))

    def _show_real_progress(self):
        progress_bar = st.progress(0)
        for percent in [20, 50, 80, 100]:
            progress_bar.progress(percent)
            time.sleep(0.3)
        progress_bar.empty()

    def _add_tts_to_history(self, text, language_name):
        if not text.strip():
            return st.warning(get_translation(st.session_state.lang, "tts_unavailable"))
        
        # Mapeamento de nomes de idioma para códigos
        lang_map = {
            'Português': 'pt', 'Portuguese': 'pt', 'Portugais': 'pt', 'Portugiesisch': 'pt', 'Portugués': 'pt',
            'Inglês': 'en', 'English': 'en', 'Anglais': 'en', 'Englisch': 'en', 'Inglés': 'en',
            'Espanhol': 'es', 'Spanish': 'es', 'Espagnol': 'es', 'Spanisch': 'es', 'Español': 'es',
            'Francês': 'fr', 'French': 'fr', 'Français': 'fr', 'Französisch': 'fr', 'Francés': 'fr',
            'Alemão': 'de', 'German': 'de', 'Allemand': 'de', 'Deutsch': 'de', 'Alemán': 'de'
        }
        
        lang_code = lang_map.get(language_name, 'pt')

        # Usar cache de áudio para evitar rerun
        audio_key = f"audio_{hashlib.sha256(text.encode()).hexdigest()}_{lang_code}"
        
        if audio_key not in st.session_state:
            with st.spinner(f"🔊 {get_translation(st.session_state.lang, 'tts_loading')}"):
                audio_bytes = TextToSpeech.get_audio(text, lang_code)
                if audio_bytes:
                    st.session_state[audio_key] = audio_bytes
        
        if audio_key in st.session_state:
            audio_bytes = st.session_state[audio_key]
        else:
            st.error(f"❌ {get_translation(st.session_state.lang, 'tts_error')}")
            return
        
        # Player de áudio
        with st.expander(f"🔊 {get_translation(st.session_state.lang, 'tts_title')}", expanded=True):
            st.audio(audio_bytes, format="audio/mpeg")
            
            # Botão de download (sem alterar estado)
            lang_suffix = lang_code.upper()
            st.download_button(
                label=f"⬇️ {get_translation(st.session_state.lang, 'tts_download')}",
                data=audio_bytes,
                file_name=f"VideoMind_{lang_suffix}.mp3",
                mime="audio/mpeg",
                use_container_width=True
            )

    def setup_ui(self):
        st.markdown(Misc.custom_css(), unsafe_allow_html=True)
        
        # Mostrar sidebar primeiro
        self.show_sidebar()
        
        # Depois mostrar o conteúdo principal ou a página selecionada
        if 'active_summary' in st.session_state:
            self.show_active_summary()
        elif 'current_page' not in st.session_state or st.session_state.current_page == 'main':
            self.show_main_content()
        else:
            self.show_selected_page()

    def show_sidebar(self):
        with st.sidebar:
            st.markdown(Misc.sidebar_header(st.session_state.lang), unsafe_allow_html=True)
            
            if 'user_id' not in st.session_state:
                with st.expander(f"🔒 {get_translation(st.session_state.lang, 'login')}", expanded=True):
                    tab1, tab2 = st.tabs([
                        get_translation(st.session_state.lang, "login"),
                        get_translation(st.session_state.lang, "register")
                    ])
                    
                    with tab1:
                        with st.form("login_form"):
                            username = st.text_input(f"👤 {get_translation(st.session_state.lang, 'username')}")
                            password = st.text_input(f"🔑 {get_translation(st.session_state.lang, 'password')}", type="password")
                            if st.form_submit_button(f"🚪 {get_translation(st.session_state.lang, 'login_button')}"):
                                user_id = authenticate(username, password)
                                if user_id:
                                    st.session_state.user_id = user_id
                                    st.session_state.username = username
                                    st.rerun()
                                else:
                                    st.error(f"❌ {get_translation(st.session_state.lang, 'invalid_credentials')}")
                    
                    with tab2:
                        with st.form("register_form"):
                            new_user = st.text_input(f"👤 {get_translation(st.session_state.lang, 'username')}")
                            new_pass = st.text_input(f"🔑 {get_translation(st.session_state.lang, 'password')}", type="password")
                            confirm_pass = st.text_input(f"🔏 {get_translation(st.session_state.lang, 'confirm_password')}", type="password")
                            
                            if st.form_submit_button(f"📝 {get_translation(st.session_state.lang, 'register_button')}"):
                                if new_pass != confirm_pass:
                                    st.error(f"❌ {get_translation(st.session_state.lang, 'password_mismatch')}")
                                elif len(new_pass) < 6:
                                    st.error(f"❌ {get_translation(st.session_state.lang, 'password_length')}")
                                elif register_user(new_user, new_pass):
                                    st.success(f"✅ {get_translation(st.session_state.lang, 'account_created')}")
                                else:
                                    st.error(f"❌ {get_translation(st.session_state.lang, 'user_exists')}")
            else:
                st.write(f"👋 {get_translation(st.session_state.lang, 'welcome').format(st.session_state.username)}")
                if st.button(f"🚪 {get_translation(st.session_state.lang, 'logout')}", use_container_width=True, key="logout_btn"):
                    del st.session_state.user_id
                    del st.session_state.username
                    st.rerun()
            
            st.markdown("---")
            
            # Seletor de Idioma de Saída
            self.output_language = st.selectbox(
                f"🌐 {get_translation(st.session_state.lang, 'output_language')}",
                options=list(self.output_language_options[st.session_state.lang].keys()),
                index=0
            )
                
            # Seletor de Tamanho do Resumo
            self.detail_level = st.radio(
                f"📏 {get_translation(st.session_state.lang, 'detail_level')}", 
                options=[
                    get_translation(st.session_state.lang, "quick"),
                    get_translation(st.session_state.lang, "standard"),
                    get_translation(st.session_state.lang, "premium")
                ],
                index=1,
                horizontal=True
            )
            
            # Histórico
            if 'user_id' in st.session_state:
                st.markdown(f"### 📚 {get_translation(st.session_state.lang, 'history')}")
                history = get_history(st.session_state.user_id)
                if not history:
                    st.info(f"📭 {get_translation(st.session_state.lang, 'no_history')}")
                else:
                    for url, title, summary, language, detail_level, created in history:
                        try:
                            created_datetime = datetime.strptime(created.split('.')[0], '%Y-%m-%d %H:%M:%S')
                            date_str = created_datetime.strftime('%d/%m/%Y %H:%M')
                            
                            col1, col2 = st.columns([6, 1])
                            
                            with col1:
                                if st.button(
                                    f"📌 {title[:30]}... ({language}, {detail_level})", 
                                    key=f"btn_{url}_{language}_{detail_level}",
                                    help=f"⏳ {get_translation(st.session_state.lang, 'generated_on')} {date_str}",
                                    use_container_width=True
                                ):
                                    st.session_state.active_summary = {
                                        'url': url,
                                        'title': title,
                                        'summary': summary,
                                        'date': date_str,
                                        'language': language,
                                        'detail_level': detail_level
                                    }
                                    st.rerun()
                            
                            with col2:
                                if st.button(
                                    "🗑️", 
                                    key=f"del_{url}_{language}_{detail_level}",
                                    help=get_translation(st.session_state.lang, "delete")
                                ):
                                    remove_from_history(st.session_state.user_id, url)
                                    st.rerun()
                            
                        except Exception as e:
                            st.error(f"⚠️ {get_translation(st.session_state.lang, 'load_error')}: {str(e)}")

            st.markdown("---")
            st.markdown('<div class="language-selector-footer">', unsafe_allow_html=True)
            selected_lang = st.selectbox(
                f"🌍 {get_translation(st.session_state.lang, 'select_language')}",
                options=list(language_options.keys()),
                format_func=lambda x: f"{language_options[x]['flag']} {language_options[x]['native']}",
                index=list(language_options.keys()).index(st.session_state.lang),
                key="lang_selector_footer"
            )
            
            if selected_lang != st.session_state.lang:
                st.session_state.lang = selected_lang
                st.rerun()

            st.markdown("---")

            st.markdown(f"### ℹ️ {get_translation(st.session_state.lang, 'help_section')}")

            page_options = {
                "tutorial": f"📘 {get_translation(st.session_state.lang, 'page_tutorial')}",
                "why_use": f"🚀 {get_translation(st.session_state.lang, 'page_why_use')}",
                "faq": f"❓ {get_translation(st.session_state.lang, 'page_faq')}",
                "privacy": f"🔒 {get_translation(st.session_state.lang, 'page_privacy')}"
            }
            
            for page, label in page_options.items():
                if st.button(label, key=f"sidebar_btn_{page}", use_container_width=True):
                    st.session_state.current_page = page
                    st.rerun()
            
                
            st.markdown('</div>', unsafe_allow_html=True)
            Misc.footer(st.session_state.lang)

    def show_main_content(self):
        """Mostra o conteúdo principal da aplicação"""
        # Carrega CSS
        st.markdown(Misc.main_page_css(), unsafe_allow_html=True)

        # Hero Section
        st.markdown(f"""
        <div class="vm-hero">
            <h1 style="margin:0; font-size:2rem">🎬 {get_translation(st.session_state.lang, "main_header")}</h1>
            <p style="margin:0.3rem 0 0; font-size:1.1rem; opacity:0.95">
                {get_translation(st.session_state.lang, "main_subheader")}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Container de Input
        with st.container():
            st.markdown('<div class="vm-input-container">', unsafe_allow_html=True)
            self.youtube_url = st.text_input(
                f"🔗 {get_translation(st.session_state.lang, 'url_label')}",
                placeholder=get_translation(st.session_state.lang, "url_placeholder"),
                key="yt_url_main"
            )
            st.markdown('</div>', unsafe_allow_html=True)

            if self.youtube_url:
                st.session_state.youtube_url = self.youtube_url
                with st.container():
                    st.markdown('<div class="vm-results-container">', unsafe_allow_html=True)
                    self.process_video()
                    st.markdown('</div>', unsafe_allow_html=True)

            # Features Grid com traduções
            st.markdown(f"""
            <div class="vm-features">
                <div class="vm-feature-card">
                    <div class="vm-feature-icon">⏱️</div>
                    <h3>{get_translation(st.session_state.lang, 'quick_summaries')}</h3>
                    <p>{get_translation(st.session_state.lang, 'quick_summaries_desc')}</p>
                </div>
                <div class="vm-feature-card">
                    <div class="vm-feature-icon">🌍</div>
                    <h3>{get_translation(st.session_state.lang, 'multilingual')}</h3>
                    <p>{get_translation(st.session_state.lang, 'multilingual_desc')}</p>
                </div>
                <div class="vm-feature-card">
                    <div class="vm-feature-icon">🎧</div>
                    <h3>{get_translation(st.session_state.lang, 'audio_text')}</h3>
                    <p>{get_translation(st.session_state.lang, 'audio_text_desc')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Call-to-Action traduzido
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align:center; margin:2.5rem 0">
            <h3>{get_translation(st.session_state.lang, 'ready_to_transform')}</h3>
            <p>{get_translation(st.session_state.lang, 'start_now')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Footer traduzido
        Misc.footer(st.session_state.lang)


    def show_selected_page(self):
        """Mostra a página selecionada com botão de voltar"""
        col1, col2 = st.columns([1, 11])
        with col1:
            if st.button(get_translation(st.session_state.lang, "back_button"), key="back_selected_page"):
                st.session_state.current_page = 'main'
                st.rerun()
        
        with col2:
            if st.session_state.current_page == 'tutorial':
                tutorial_page.tutorial_page()
            elif st.session_state.current_page == 'why_use':
                why_use_page.why_use_page()
            elif st.session_state.current_page == 'faq':
                faq_page.faq_page()
            elif st.session_state.current_page == 'privacy':
                privacy_page.privacy_page()
        Misc.footer(st.session_state.lang)

    def show_active_summary(self):
        data = st.session_state.active_summary
        video_id = GetVideo.extract_video_id(data['url'])
        
        col1, col2 = st.columns([1, 11])
        with col1:
            if st.button(get_translation(st.session_state.lang, "back_button"), key="back_active_summary"):
                del st.session_state.active_summary
                st.rerun()
        with col2:
            st.subheader(f"📌 {data['title']} ({data['language']}, {data['detail_level']})")
            st.caption(f"⏳ {get_translation(st.session_state.lang, 'generated_on')} {data['date']}")
        
        col_img, col_content = st.columns([1, 2])
        
        with col_img:
            self._embed_video_preview(video_id)
        
        with col_content:
            st.markdown(data['summary'])
            create_action_buttons(data['summary'], data['title'], st.session_state.lang)
            self._add_tts_to_history(data['summary'], data['language'])

    def process_video(self):
        try:
            if not st.session_state.youtube_url:
                return
                    
            self._show_real_progress()
            self.video_id = GetVideo.extract_video_id(st.session_state.youtube_url)
            self.video_title = GetVideo.title(st.session_state.youtube_url)
            
            # Container do vídeo
            with st.container():
                self._embed_video_preview(self.video_id)
            
            # Tabs originais (mantenha seu código existente aqui)
            tab1, tab2, tab3 = st.tabs([
                f"📖 {get_translation(st.session_state.lang, 'summary_tab')}",
                f"⏱️ {get_translation(st.session_state.lang, 'timestamps_tab')}",
                f"📜 {get_translation(st.session_state.lang, 'transcript_tab')}"
            ])
            
            with tab1:
                self.generate_summary()
            
            with tab2:
                self.generate_timestamps()
            
            with tab3:
                self.generate_transcript()

        except Exception as e:
            st.error(f"⚠️ {get_translation(st.session_state.lang, 'video_error')}: {str(e)}")

    def generate_summary(self):
        if st.button(f"✨ {get_translation(st.session_state.lang, 'generate_summary')}", type="primary", key="generate_btn"):
            with st.spinner(f"🔍 {get_translation(st.session_state.lang, 'analyzing')}"):
                try:
                    transcript = GetVideo.transcript(st.session_state.youtube_url)
                    
                    if not transcript:
                        st.warning(f"⚠️ {get_translation(st.session_state.lang, 'no_transcript')}")
                        return
                    
                    target_lang_name = self.output_language
                    target_lang_code = self._get_output_language_code()
                    detail_level = self.detail_level.lower()
                    
                    # Verificar cache
                    cached_summary = None
                    if 'user_id' in st.session_state:
                        cached_summary = get_cached_summary(
                            st.session_state.user_id,
                            self.video_id,
                            target_lang_code,
                            detail_level
                        )
                    
                    if cached_summary:
                        st.info(f"🔁 {get_translation(st.session_state.lang, 'cached_summary')} ({target_lang_name}, {detail_level})")
                        summary_text = cached_summary
                        
                        # Verificar se o resumo está no histórico e adicionar se não estiver
                        history = get_history(st.session_state.user_id)
                        url_in_history = any(item[0] == st.session_state.youtube_url and 
                                            item[3] == target_lang_name and 
                                            item[4] == detail_level 
                                            for item in history)
                        
                        if not url_in_history:
                            save_history(
                                st.session_state.user_id,
                                st.session_state.youtube_url,
                                self.video_title,
                                summary_text,
                                target_lang_name,
                                detail_level
                            )
                    else:
                        prompt = Prompt.createSummaryPrompt(transcript, target_lang_code, detail_level)
                        result = Model.google_gemini(transcript, prompt)
                        summary_text = result
                        
                        if 'user_id' in st.session_state:
                            save_history(
                                st.session_state.user_id,
                                st.session_state.youtube_url,
                                self.video_title,
                                result,
                                target_lang_name,
                                detail_level
                            )
                            save_to_cache(
                                st.session_state.user_id,
                                self.video_id,
                                result,
                                target_lang_code,
                                detail_level
                            )
                except Exception as e:
                    st.error(f"⚠️ {get_translation(st.session_state.lang, 'video_error')}: {str(e)}")
                    return
            
            # Exibir resumo fora do spinner
            st.markdown(f"### 📌 {get_translation(st.session_state.lang, 'summary_title')} ({target_lang_name}, {detail_level})")
            st.markdown(summary_text)
            
            # Adicionar botões de ação
            create_action_buttons(summary_text, self.video_title, st.session_state.lang)
            
            # Adicionar TTS (com seu próprio spinner)
            self._add_tts_to_history(summary_text, target_lang_name)

    def generate_timestamps(self):
        if st.button(f"⏱️ {get_translation(st.session_state.lang, 'generate_timestamps')}", type="primary"):
            with st.spinner(f"🔄 {get_translation(st.session_state.lang, 'processing')}"):
                transcript = GetVideo.transcript_time(st.session_state.youtube_url)
                
                if not transcript:
                    st.warning(f"⚠️ {get_translation(st.session_state.lang, 'no_transcript')}")
                    return
                    
                target_lang_code = self._get_output_language_code()
                prompt = Prompt.createTimestampPrompt(
                    transcript,
                    self.video_id,
                    target_lang_code
                )
                result = Model.google_gemini(transcript, prompt)
                
                st.markdown(f"### 🕒 {get_translation(st.session_state.lang, 'timeline_title')}")
                st.markdown(self.format_timestamps(result, self.video_id), unsafe_allow_html=True)

    def generate_transcript(self):
        transcript = GetVideo.transcript(st.session_state.youtube_url)
        
        if not transcript:
            st.warning(f"⚠️ {get_translation(st.session_state.lang, 'no_transcript')}")
            return
        
        # Mapeamento FIXO de códigos para nomes de idiomas
        language_map = {
            'pt': 'Português',
            'en': 'Inglês',
            'es': 'Espanhol',
            'fr': 'Francês',
            'de': 'Alemão'
        }
        
        video_lang_code = GetVideo.detect_language(transcript)
        video_lang_name = language_map.get(video_lang_code, 'Inglês')
        
        # Obter código do idioma de saída
        target_lang_code = self._get_output_language_code()
        target_lang_name = language_map.get(target_lang_code, 'Inglês')

        # Se o idioma de saída for diferente do idioma original
        if target_lang_code != video_lang_code:
            view_options = [
                get_translation(st.session_state.lang, "original"),
                get_translation(st.session_state.lang, "translated_only"),
                get_translation(st.session_state.lang, "bilingual")
            ]
            
            selected_view = st.radio(
                f"👁️ {get_translation(st.session_state.lang, 'view_mode')}",
                options=view_options,
                horizontal=True,
                key="transcript_view_mode"
            )
        else:
            selected_view = get_translation(st.session_state.lang, "original")

        if st.button(f"📜 {get_translation(st.session_state.lang, 'generate_transcript')}", type="primary"):
            with st.spinner(f"🔄 {get_translation(st.session_state.lang, 'processing')}"):
                if selected_view == get_translation(st.session_state.lang, "original"):
                    st.markdown(f"### 📜 {get_translation(st.session_state.lang, 'original_transcript')} ({video_lang_name})")
                    st.markdown(transcript)
                
                else:
                    # Traduzir usando o código do idioma
                    translated = Model.google_gemini(
                        transcript,
                        Prompt.createTranscriptPrompt(transcript, target_lang_code)
                    )
                    
                    if selected_view == get_translation(st.session_state.lang, "translated_only"):
                        st.markdown(f"### 🌐 {get_translation(st.session_state.lang, 'translated_transcript')} ({target_lang_name})")
                        st.markdown(translated)
                    
                    else:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"### 🌍 {get_translation(st.session_state.lang, 'original_transcript')} ({video_lang_name})")
                            st.markdown(transcript)
                        with col2:
                            st.markdown(f"### 🌐 {get_translation(st.session_state.lang, 'translated_transcript')} ({target_lang_name})")
                            st.markdown(translated)

    def format_timestamps(self, text: str, video_id: str) -> str:
        def replacer(match):
            h, m, s = map(int, match.groups())
            total_sec = h * 3600 + m * 60 + s
            return f'<a href="https://youtu.be/{video_id}?t={total_sec}" class="timestamp-link">{h:02d}:{m:02d}:{s:02d}</a>'
        
        lines = text.split('\n')
        formatted_lines = []
        for line in lines:
            formatted_line = re.sub(r'\[(\d+):(\d+):(\d+)\]', replacer, line)
            formatted_lines.append(f'<div class="timestamp-item">{formatted_line}</div>')
        
        return f'<div class="timestamp-container">{"".join(formatted_lines)}</div>'

    def _get_output_language_code(self):
        """Obtém código ISO """
        selected_option = self.output_language
        lang_map = self.output_language_options[st.session_state.lang]
        return lang_map[selected_option]

# =============================================
# INICIALIZAÇÃO
# =============================================
if __name__ == "__main__":
    AIVideoSummarizer()