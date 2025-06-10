import base64
import streamlit.components.v1 as components
from src.translations import get_translation

def create_action_buttons(content: str, title: str, lang: str) -> None:
    """Cria botões de ação (copiar e download) estilizados"""
    if not content:
        return
        
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    copy_text = get_translation(lang, "copy")
    copied_text = get_translation(lang, "copied")
    download_text = get_translation(lang, "download")

    components.html(f"""
    <style>
        .action-section {{
            margin: 2rem 0;
            padding: 1rem 0;
            width: 100%;
        }}
        
        .action-buttons {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            width: 100%;
        }}
        
        .action-btn {{
            padding: 0.75rem;
            border-radius: 8px;
            border: none;
            font-weight: 500;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.9rem;
            text-decoration: none !important;
            width: 100%;
            box-sizing: border-box;
        }}
        
        .copy-btn {{
            background: #4f46e5;
            color: white !important;
        }}
        
        .download-btn {{
            background: #10b981;
            color: white !important;
        }}
        
        @media (max-width: 400px) {{
            .action-buttons {{
                grid-template-columns: 1fr;
            }}
            
            .action-btn {{
                padding: 0.75rem 0.5rem;
                font-size: 0.85rem;
            }}
        }}
    </style>

    <div class="action-section">
        <div class="action-buttons">
            <button onclick="copyToClipboard()" class="action-btn copy-btn">
                📋 {copy_text}
            </button>
            
            <a href="data:text/plain;base64,{encoded_content}" 
            download="VideoMind_{title[:20]}.txt" 
            class="action-btn download-btn">
                ⏬ {download_text}
            </a>
        </div>
    </div>

    <textarea id="copyContent" style="opacity: 0; position: absolute; left: -9999px;">{content}</textarea>
    
    <script>
        function copyToClipboard() {{
            const element = document.getElementById('copyContent');
            element.select();
            document.execCommand('copy');
            const btn = event.currentTarget;
            btn.innerHTML = `✓ {copied_text}`;
            setTimeout(() => {{
                btn.innerHTML = `📋 {copy_text}`;
            }}, 2000);
        }}
    </script>
    """, height=100)