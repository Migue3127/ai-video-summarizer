from src.translations import get_translation
import streamlit as st

class Misc:
    @staticmethod
    def main_header(lang='pt'):
        return f"""
        <div class="header">
            <h1 style="margin: 0; font-size: 1.8rem;">
                {get_translation(lang, "main_header")}
            </h1>
            <p style="margin: 0.5rem 0 0; opacity: 0.9;">
                {get_translation(lang, "main_subheader")}
            </p>
        </div>
        """
    
    @staticmethod
    def sidebar_header(lang='pt'):
        st.image("assets/logo.png", use_container_width=True)
        return f"""
        <div style="text-align: center; margin-bottom: 2rem; padding: 1rem 0;">
            <h1 style="color: #4f46e5; font-size: 1.5rem; margin-bottom: 0.5rem;">
                {get_translation(lang, "app_title")}
            </h1>
            <p style="color: #64748b; font-size: 0.9rem;">
                {get_translation(lang, "app_subtitle")}
            </p>
        </div>
        """

    @staticmethod
    def custom_css():
        return """
        <style>
            /* RESET DO LAYOUT */
            .stApp {
                margin-left: 0 !important;
                padding: 0 !important;
            }
            
            /* VIDEO CONTAINER */
            .video-container {
                position: relative;
                width: 100%;
                padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
                margin: 1rem 0;
                border-radius: 12px;
                overflow: hidden;
            }
            
            .video-container iframe {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: none;
            }

            .hidden-slider {
                display: none !important;
                visibility: hidden !important;
                height: 0 !important;
                width: 0 !important;
                opacity: 0 !important;
                position: absolute !important;
                left: -9999px !important;
            }
            
            /* SIDEBAR FIXA E RESPONSIVA */
            section[data-testid="stSidebar"] {
                background: #f8f9fa !important;
                border-right: 1px solid #e2e8f0 !important;
                width: 300px !important;
                left: 0 !important;
                top: 0 !important;
                height: 100vh;
                transition: all 0.3s;
                box-shadow: none !important;
            }
            
            /* CONTEÚDO PRINCIPAL */
            .main .block-container {
                margin-left: 300px !important;
                padding: 2rem 3rem;
                max-width: 100% !important;
            }
            
            /* HEADER PRINCIPAL */
            .header {
                background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
                color: white;
                padding: 2rem;
                border-radius: 12px;
                margin-bottom: 2rem;
            }
            
            /* BOTÕES DE AÇÃO */
            .action-buttons-container {
                display: flex !important;
                gap: 12px;
                margin-top: 20px;
                align-items: center;
                opacity: 1 !important;
                visibility: visible !important;
            }
            
            /* RESPONSIVIDADE (MOBILE) */
            @media (max-width: 768px) {
                section[data-testid="stSidebar"] {
                    width: 85% !important;
                    transform: translateX(-100%);
                    transition: transform 0.3s;
                    height: 100vh;
                    position: fixed;
                    z-index: 1000;
                }
                
                section[data-testid="stSidebar"].sidebar-visible {
                    transform: translateX(0);
                }
                
                .main .block-container {
                    margin-left: 0 !important;
                    padding: 1rem;
                }
                
                .video-container {
                    margin: 0.5rem 0;
                }
            }
             /* AJUSTE PARA BOTÃO DE LIXO */
            .vm-trash-button {
                margin-left: -12px !important;
                padding: 0 8px !important;
                min-width: 32px !important;
                border: none !important;
                background: transparent !important;
                color: #ef4444 !important;
            }
            
            .vm-trash-button:hover {
                background: rgba(239, 68, 68, 0.1) !important;
                transform: scale(1.05);
            }
            
            /* AJUSTE DE LAYOUT PARA HISTÓRICO */
            .history-item {
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 8px;
            }
            
            .history-title {
                flex-grow: 1;
                overflow: hidden;
                text-overflow: ellipsis;
            }

            /* evitar sobreposição */
            .stApp {
                padding-bottom: 150px !important;
            }
            
            /* Ajuste para mobile */
            @media (max-width: 768px) {
                .stApp {
                    padding-bottom: 200px !important;
                }
            }

            /* Espaçamento para o footer */
            .stApp {
                padding-bottom: 150px !important;
            }
            
            /* Ajuste para páginas de conteúdo */
            .page-content {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            
            /* Ajuste para mobile */
            @media (max-width: 768px) {
                .stApp {
                    padding-bottom: 200px !important;
                }
            }

            /* Adicione ao custom_css() em misc.py */
            .stSidebar [href*="page="] {
                display: none !important;
            }

            /* Estilo para os botões de ajuda na sidebar */
            .vm-help-btn {
                width: 100%;
                text-align: left;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                margin: 0.25rem 0;
                transition: all 0.2s;
                background: transparent;
                border: none;
                color: #4f46e5;
            }

            .vm-help-btn:hover {
                background: rgba(79, 70, 229, 0.1);
            }

            /* Remover padding extra do footer */
            .stApp {
                padding-bottom: 20px !important;
            }

            /* Estilo para os botões de navegação */
            .vm-nav-btn {
                width: 100%;
                text-align: left;
                padding: 0.75rem 1rem;
                border-radius: 8px;
                margin: 0.25rem 0;
                transition: all 0.2s;
                background: rgba(79, 70, 229, 0.1);
                border: 1px solid rgba(79, 70, 229, 0.2);
                color: #4f46e5;
            }

            .vm-nav-btn:hover {
                background: rgba(79, 70, 229, 0.2);
            }

            /* Espaçamento para o conteúdo das páginas */
            .page-container {
                padding: 1rem 2rem;
            }

            /* Garantir que o conteúdo principal não fique escondido */
            .main .block-container {
                padding-bottom: 2rem !important;
            }

            /* Estilo para os botões de navegação */
            .stButton>button {
                transition: all 0.3s !important;
            }

            .stButton>button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
            }
        </style>
        """
    @staticmethod
    def footer(lang='pt'):
        copyright_text = get_translation(lang, "footer_copyright")
        st.markdown(
            f"""
            <style>
                .footer {{
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    width: 100%;
                    background-color: #f8f9fa;
                    padding: 15px;
                    text-align: center;
                    border-top: 1px solid #e2e8f0;
                    z-index: 100;
                    font-size: 0.85rem;
                    line-height: 1.6;
                    transition: all 0.3s ease;
                }}

                [data-testid="stSidebar"][aria-expanded="false"] ~ .main .footer {{
                    width: 100%;
                    margin-left: 0;
                }}

                @media (max-width: 768px) {{
                    .footer {{
                        width: 100%;
                        margin-left: 0;
                    }}

                    .footer-links {{
                        flex-wrap: wrap;
                    }}
                }}
            </style>
            <div class="footer">
                <div>{copyright_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def main_page_css():
        return """
        <style>
            /* Hero Section */
            .vm-hero {
                background: linear-gradient(135deg, #4f46e5 0%, #8b5cf6 100%);
                padding: 2.5rem;
                border-radius: 16px;
                color: white;
                margin-bottom: 2rem;
                position: relative;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(110, 72, 170, 0.3);
            }
            .vm-hero::after {
                content: "";
                position: absolute;
                top: 80px;
                right: -50px;
                width: 150px;
                height: 150px;
                background: url('https://cdn-icons-png.flaticon.com/512/2491/2491916.png') no-repeat;
                background-size: contain;
                opacity: 0.1;
            }
            
            /* Video Results Container */
            .vm-results-container {
                background: white;
                border-radius: 12px;
                padding: 2rem;
                box-shadow: 0 5px 25px rgba(0,0,0,0.08);
                margin-top: 2rem;
                display: none; /* Inicialmente oculto */
            }
            
            /* Features Grid */
            .vm-features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
                margin: 2.5rem 0;
            }
            .vm-feature-card {
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                border-left: 4px solid #6e48aa;
                transition: all 0.3s ease;
            }
            .vm-feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            }
            .vm-feature-icon {
                font-size: 1.8rem;
                margin-bottom: 0.8rem;
                color: #6e48aa;
            }
        </style>
        """