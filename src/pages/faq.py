import streamlit as st
from src.translations import get_translation

def faq_page():
    # Configuração de estilo
    st.markdown("""
    <style>
        .faq-container {
            max-width: 800px;
            margin: 0 auto;
        }
        .faq-question {
            background-color: #f8f9fa;
            padding: 1.2rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border-left: 4px solid #4f46e5;
            transition: all 0.3s ease;
        }
        .faq-question:hover {
            background-color: #f1f5fe;
            transform: translateX(5px);
        }
        .faq-answer {
            padding: 1rem 1.5rem;
            background-color: white;
            border-radius: 8px;
            margin-top: 0.5rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        .faq-category {
            color: #4f46e5;
            margin-top: 2rem;
            margin-bottom: 1rem;
            font-size: 1.3rem;
            font-weight: 600;
        }
        .faq-badge {
            background-color: #e0e7ff;
            color: #4f46e5;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 0.8rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Container principal
    with st.container():
        st.title(f"❓ {get_translation(st.session_state.lang, 'faq_title')}")
        st.markdown("---")
        
        # Barra de busca
        search_query = st.text_input(
            f"🔍 {get_translation(st.session_state.lang, 'search_faq')}", 
            placeholder=get_translation(st.session_state.lang, "search_placeholder")
        )
        
        # Categorias de perguntas
        with st.expander(f"📚 {get_translation(st.session_state.lang, 'browse_categories')}", expanded=True):
            cols = st.columns(4)
            with cols[0]:
                if st.button(get_translation(st.session_state.lang, "general"), use_container_width=True):
                    st.session_state.faq_category = "geral"
            with cols[1]:
                if st.button(get_translation(st.session_state.lang, "features"), use_container_width=True):
                    st.session_state.faq_category = "funcionalidades"
            with cols[2]:
                if st.button(get_translation(st.session_state.lang, "privacy"), use_container_width=True):
                    st.session_state.faq_category = "privacidade"
            with cols[3]:
                if st.button(get_translation(st.session_state.lang, "technical"), use_container_width=True):
                    st.session_state.faq_category = "tecnico"
        
        st.markdown("---")
        
        # Todas as FAQs organizadas
        faqs = {
            "geral": [
                {
                    "question": get_translation(st.session_state.lang, "faq_q1"),
                    "answer": get_translation(st.session_state.lang, "faq_a1"),
                    "tags": ["vídeos", "suporte"]
                },
                {
                    "question": get_translation(st.session_state.lang, "faq_q2"),
                    "answer": get_translation(st.session_state.lang, "faq_a2"),
                    "tags": ["idiomas", "tradução"]
                }
            ],
            "funcionalidades": [
                {
                    "question": get_translation(st.session_state.lang, "faq_q3"),
                    "answer": get_translation(st.session_state.lang, "faq_a3"),
                    "tags": ["áudio", "TTS"]
                },
                {
                    "question": get_translation(st.session_state.lang, "faq_q4"),
                    "answer": get_translation(st.session_state.lang, "faq_a4"),
                    "tags": ["tradução", "transcrição"]
                }
            ],
            "privacidade": [
                {
                    "question": get_translation(st.session_state.lang, "faq_q5"),
                    "answer": get_translation(st.session_state.lang, "faq_a5"),
                    "tags": ["dados", "segurança"]
                },
                {
                    "question": get_translation(st.session_state.lang, "faq_q6"),
                    "answer": get_translation(st.session_state.lang, "faq_a6"),
                    "tags": ["YouTube", "termos"]
                }
            ],
            "tecnico": [
                {
                    "question": get_translation(st.session_state.lang, "faq_q7"),
                    "answer": get_translation(st.session_state.lang, "faq_a7"),
                    "tags": ["limites", "duração"]
                },
                {
                    "question": get_translation(st.session_state.lang, "faq_q8"),
                    "answer": get_translation(st.session_state.lang, "faq_a8"),
                    "tags": ["transcrição", "erros"]
                }
            ]
        }

        # Filtro por categoria
        selected_category = st.session_state.get('faq_category', 'geral')
        
        # Exibição das FAQs
        st.markdown(f'<div class="faq-category">{get_translation(st.session_state.lang, selected_category)}</div>', unsafe_allow_html=True)
        
        displayed_questions = 0
        
        for faq in faqs.get(selected_category, []):
            # Filtro por busca
            if search_query:
                search_terms = search_query.lower().split()
                question_text = faq["question"].lower()
                answer_text = faq["answer"].lower()
                tags_text = " ".join(faq["tags"]).lower()
                
                if not any(term in question_text or term in answer_text or term in tags_text for term in search_terms):
                    continue
            
            with st.container():
                st.markdown(f'<div class="faq-question"><strong>{faq["question"]}</strong></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="faq-answer">{faq["answer"]}</div>', unsafe_allow_html=True)
                
                # Tags
                tags_html = " ".join([f'<span class="faq-badge">{tag}</span>' for tag in faq["tags"]])
                st.markdown(f'<div style="margin-top: 0.5rem;">{tags_html}</div>', unsafe_allow_html=True)
                
                displayed_questions += 1
        
        if displayed_questions == 0:
            st.warning(get_translation(st.session_state.lang, "no_results"))