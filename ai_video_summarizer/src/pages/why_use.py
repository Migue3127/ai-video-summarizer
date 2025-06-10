import streamlit as st
from src.translations import get_translation
import time

def why_use_page():
    # Configuração de estilo premium
    st.markdown("""
    <style>
        .why-use-container {
            max-width: 1000px;
            margin: 0 auto;
        }
        .hero-section {
            background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
            color: white;
            padding: 3rem;
            border-radius: 16px;
            margin-bottom: 3rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .hero-section::after {
            content: "";
            position: absolute;
            bottom: -50px;
            right: -50px;
            width: 200px;
            height: 200px;
            background: url('https://cdn-icons-png.flaticon.com/512/2491/2491916.png') no-repeat;
            background-size: contain;
            opacity: 0.1;
        }
        .benefit-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            border: none;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1);
            position: relative;
            overflow: hidden;
        }
        .benefit-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.12);
        }
        .benefit-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, #4f46e5, #818cf8);
        }
        .benefit-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: #4f46e5;
        }
        .stat-container {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 1rem;
            margin: 3rem 0;
        }
        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            min-width: 200px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            flex: 1;
        }
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #4f46e5;
            margin-bottom: 0.5rem;
            line-height: 1;
        }
        .stat-label {
            font-size: 0.9rem;
            color: #64748b;
        }
        .testimonial-section {
            background: #f8fafc;
            border-radius: 16px;
            padding: 2rem;
            margin: 3rem 0;
            position: relative;
        }
        .testimonial-quote {
            font-size: 1.2rem;
            font-style: italic;
            color: #334155;
            position: relative;
            padding-left: 2rem;
        }
        .testimonial-quote::before {
            content: "“";
            position: absolute;
            left: 0;
            top: -1rem;
            font-size: 4rem;
            color: #c7d2fe;
            font-family: Georgia, serif;
        }
        .testimonial-author {
            display: flex;
            align-items: center;
            margin-top: 1.5rem;
        }
        .author-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            object-fit: cover;
            margin-right: 1rem;
            border: 3px solid #e0e7ff;
        }
        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
        }
        .comparison-table th, .comparison-table td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }
        .comparison-table th {
            background-color: #f1f5f9;
            font-weight: 600;
        }
        .comparison-table tr:last-child td {
            border-bottom: none;
        }
        .feature-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
        .feature-badge-primary {
            background-color: #e0e7ff;
            color: #4f46e5;
        }
        .feature-badge-secondary {
            background-color: #ecfdf5;
            color: #059669;
        }
        .cta-section {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            padding: 3rem;
            border-radius: 16px;
            text-align: center;
            margin: 3rem 0;
        }
        .cta-button {
            display: inline-block;
            background: white;
            color: #4f46e5;
            padding: 1rem 2rem;
            border-radius: 50px;
            font-weight: 600;
            text-decoration: none;
            margin-top: 1.5rem;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        .animated-underline {
            display: inline-block;
            position: relative;
        }
        .animated-underline::after {
            content: '';
            position: absolute;
            width: 100%;
            transform: scaleX(0);
            height: 3px;
            bottom: -5px;
            left: 0;
            background: linear-gradient(90deg, #4f46e5, #8b5cf6);
            transform-origin: bottom right;
            transition: transform 0.5s cubic-bezier(0.86, 0, 0.07, 1);
        }
        .animated-underline:hover::after {
            transform: scaleX(1);
            transform-origin: bottom left;
        }
    </style>
    """, unsafe_allow_html=True)

    # Container principal
    with st.container():
        # Hero Section
        st.markdown(f"""
        <div class="hero-section">
            <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">{get_translation(st.session_state.lang, "why_use_hero_title")}</h1>
            <p style="font-size: 1.2rem; opacity: 0.9; max-width: 800px; margin: 0 auto;">
                {get_translation(st.session_state.lang, "why_use_hero_subtitle")}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Impactful statistics
        st.markdown(f"""
        <div class="stat-container">
            <div class="stat-card">
                <div class="stat-number">+87%</div>
                <div class="stat-label">{get_translation(st.session_state.lang, "retention_rate")}</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">10x</div>
                <div class="stat-label">{get_translation(st.session_state.lang, "more_efficient")}</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">5</div>
                <div class="stat-label">{get_translation(st.session_state.lang, "supported_languages")}</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">∞</div>
                <div class="stat-label">{get_translation(st.session_state.lang, "possibilities")}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Main benefits
        st.markdown(f"""
        <h2 style="text-align: center; margin-bottom: 2rem; color: #1e293b;">
            {get_translation(st.session_state.lang, "why_choose_videomind")}
        </h2>
        """, unsafe_allow_html=True)

        # Benefit 1 - Time Saving
        st.markdown(f"""
        <div class="benefit-card">
            <div class="benefit-icon">⏳</div>
            <h3 style="margin-top: 0; color: #1e293b;">{get_translation(st.session_state.lang, "time_saving_title")}</h3>
            <p style="color: #64748b; line-height: 1.6;">
                {get_translation(st.session_state.lang, "time_saving_description")}
            </p>
            <div style="margin-top: 1.5rem;">
                <span class="feature-badge feature-badge-primary">{get_translation(st.session_state.lang, "smart_processing")}</span>
                <span class="feature-badge feature-badge-primary">{get_translation(st.session_state.lang, "focus_essentials")}</span>
                <span class="feature-badge feature-badge-primary">{get_translation(st.session_state.lang, "hierarchical_summaries")}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Benefit 2 - Deep Learning
        st.markdown(f"""
        <div class="benefit-card">
            <div class="benefit-icon">🧠</div>
            <h3 style="margin-top: 0; color: #1e293b;">{get_translation(st.session_state.lang, "effective_learning_title")}</h3>
            <p style="color: #64748b; line-height: 1.6;">
                {get_translation(st.session_state.lang, "effective_learning_description")}
            </p>
            <div style="margin-top: 1.5rem;">
                <span class="feature-badge feature-badge-secondary">{get_translation(st.session_state.lang, "cognitive_structure")}</span>
                <span class="feature-badge feature-badge-secondary">{get_translation(st.session_state.lang, "integrated_mindmap")}</span>
                <span class="feature-badge feature-badge-secondary">{get_translation(st.session_state.lang, "spaced_repetition")}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Benefit 3 - Multilingual
        st.markdown(f"""
        <div class="benefit-card">
            <div class="benefit-icon">🌍</div>
            <h3 style="margin-top: 0; color: #1e293b;">{get_translation(st.session_state.lang, "multilingual_title")}</h3>
            <p style="color: #64748b; line-height: 1.6;">
                {get_translation(st.session_state.lang, "multilingual_description")}
            </p>
            <div style="margin-top: 1.5rem;">
                <span class="feature-badge">🇵🇹 {get_translation(st.session_state.lang, "portuguese")}</span>
                <span class="feature-badge">🇬🇧 {get_translation(st.session_state.lang, "english")}</span>
                <span class="feature-badge">🇪🇸 {get_translation(st.session_state.lang, "spanish")}</span>
                <span class="feature-badge">🇫🇷 {get_translation(st.session_state.lang, "french")}</span>
                <span class="feature-badge">🇩🇪 {get_translation(st.session_state.lang, "german")}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <h2 style="text-align: center; margin: 3rem 0 1.5rem; color: #1e293b;">
            {get_translation(st.session_state.lang, "comparison_title")}
        </h2>
        
        <table class="comparison-table">
            <tr>
                <th style="width: 40%;">{get_translation(st.session_state.lang, "category")}</th>
                <th style="text-align: center;">{get_translation(st.session_state.lang, "traditional_method")}</th>
                <th style="text-align: center;">VideoMind PRO</th>
            </tr>
            <tr>
                <td>{get_translation(st.session_state.lang, "time_to_summarize")}</td>
                <td style="text-align: center;">60-90 {get_translation(st.session_state.lang, "minutes")}</td>
                <td style="text-align: center; color: #4f46e5; font-weight: 600;">2 {get_translation(st.session_state.lang, "minutes")}</td>
            </tr>
            <tr>
                <td>{get_translation(st.session_state.lang, "retention_after_week")}</td>
                <td style="text-align: center;">~20%</td>
                <td style="text-align: center; color: #4f46e5; font-weight: 600;">~75%</td>
            </tr>
            <tr>
                <td>{get_translation(st.session_state.lang, "key_concept_analysis")}</td>
                <td style="text-align: center;">{get_translation(st.session_state.lang, "manual_subjective")}</td>
                <td style="text-align: center; color: #4f46e5; font-weight: 600;">{get_translation(st.session_state.lang, "ai_accurate")}</td>
            </tr>
            <tr>
                <td>{get_translation(st.session_state.lang, "accessibility")}</td>
                <td style="text-align: center;">{get_translation(st.session_state.lang, "depends_original_language")}</td>
                <td style="text-align: center; color: #4f46e5; font-weight: 600;">5 {get_translation(st.session_state.lang, "languages_available")}</td>
            </tr>
            <tr>
                <td>{get_translation(st.session_state.lang, "opportunity_cost")}</td>
                <td style="text-align: center;">{get_translation(st.session_state.lang, "high")}</td>
                <td style="text-align: center; color: #4f46e5; font-weight: 600;">{get_translation(st.session_state.lang, "very_low")}</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)

        # Testimonials
        st.markdown(f"""
        <div class="testimonial-section">
            <div class="testimonial-quote">
                {get_translation(st.session_state.lang, "testimonial_quote")}
            </div>
            <div class="testimonial-author">
                <img src="https://randomuser.me/api/portraits/women/43.jpg" class="author-avatar">
                <div>
                    <div style="font-weight: 600;">{get_translation(st.session_state.lang, "testimonial_author")}</div>
                    <div style="color: #64748b; font-size: 0.9rem;">{get_translation(st.session_state.lang, "testimonial_position")}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Use cases
        st.markdown(f"""
        <h2 style="text-align: center; margin: 3rem 0 1.5rem; color: #1e293b;">
            {get_translation(st.session_state.lang, "boost_productivity")}
        </h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
            <div style="background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                <h4 style="margin-top: 0; color: #4f46e5;">🎓 {get_translation(st.session_state.lang, "education")}</h4>
                <ul style="color: #64748b;">
                    <li>{get_translation(st.session_state.lang, "summarize_classes")}</li>
                    <li>{get_translation(st.session_state.lang, "exam_prep")}</li>
                    <li>{get_translation(st.session_state.lang, "academic_research")}</li>
                    <li>{get_translation(st.session_state.lang, "content_review")}</li>
                </ul>
            </div>
            <div style="background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                <h4 style="margin-top: 0; color: #4f46e5;">💼 {get_translation(st.session_state.lang, "professional")}</h4>
                <ul style="color: #64748b;">
                    <li>{get_translation(st.session_state.lang, "corporate_training")}</li>
                    <li>{get_translation(st.session_state.lang, "executive_reports")}</li>
                    <li>{get_translation(st.session_state.lang, "skill_updates")}</li>
                    <li>{get_translation(st.session_state.lang, "webinars_conferences")}</li>
                </ul>
            </div>
            <div style="background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                <h4 style="margin-top: 0; color: #4f46e5;">🧠 {get_translation(st.session_state.lang, "personal_development")}</h4>
                <ul style="color: #64748b;">
                    <li>{get_translation(st.session_state.lang, "online_courses")}</li>
                    <li>{get_translation(st.session_state.lang, "video_podcasts")}</li>
                    <li>{get_translation(st.session_state.lang, "complex_tutorials")}</li>
                    <li>{get_translation(st.session_state.lang, "documentaries")}</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # CTA Section
        st.markdown(f"""
        <div class="cta-section">
            <h2 style="margin-top: 0; color: white;">{get_translation(st.session_state.lang, "ready_to_revolutionize")}</h2>
            <p style="color: rgba(255,255,255,0.9); max-width: 600px; margin: 0 auto;">
                {get_translation(st.session_state.lang, "try_now_free")}
            </p>
            <a href="/" class="cta-button">{get_translation(st.session_state.lang, "get_started")} →</a>
        </div>
        """, unsafe_allow_html=True)

        # Footer
        st.markdown(f"""
        <div style="text-align: center; color: #64748b; font-size: 0.9rem; margin-top: 3rem;">
            <p>{get_translation(st.session_state.lang, "academic_project")}</p>
            <p>{get_translation(st.session_state.lang, "informatics_technician")} • 2025</p>
        </div>
        """, unsafe_allow_html=True)