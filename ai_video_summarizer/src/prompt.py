class Prompt:
    @staticmethod
    def createSummaryPrompt(text: str, targetLanguage: str, summary_type: str = "normal") -> str:
        language_mapping = {
            'pt': {  # Português
                'title': 'TÍTULO',
                'sections': ['VISÃO GERAL', 'PONTOS-CHAVE', 'PRINCIPAIS LIÇÕES', 'CONTEXTO'],
                'instruction': 'Gere um **resumo {summary_type}** em Português de Portugal com esta estrutura:'
            },
            'en': {  # Inglês
                'title': 'TITLE',
                'sections': ['OVERVIEW', 'KEY POINTS', 'MAIN TAKEAWAYS', 'CONTEXT'],
                'instruction': 'Generate a **{summary_type} summary** in English with this exact structure:'
            },
            'es': {  # Espanhol
                'title': 'TÍTULO',
                'sections': ['VISIÓN GENERAL', 'PUNTOS CLAVE', 'CONCLUSIONES', 'CONTEXTO'],
                'instruction': 'Genera un **resumen {summary_type}** en Español con:'
            },
            'fr': {  # Francês
                'title': 'TITRE',
                'sections': ['APERÇU', 'POINTS CLÉS', 'PRINCIPALES CONCLUSIONS', 'CONTEXTE'],
                'instruction': 'Produisez un **résumé {summary_type}** en Français avec:'
            },
            'de': {  # Alemão
                'title': 'TITEL',
                'sections': ['ÜBERBLICK', 'HAUPTPUNKTE', 'SCHLUSSFOLGERUNGEN', 'KONTEXT'],
                'instruction': 'Erstellen Sie eine **{summary_type} Zusammenfassung** auf Deutsch:'
            }
        }

        length_rules = {
            'curto': {
                'length': "80-120 palavras",
                'sections': ['VISÃO GERAL', 'PONTOS-CHAVE'],
                'detail': "Apenas os pontos mais essenciais"
            },
            'normal': {
                'length': "150-250 palavras",
                'sections': ['VISÃO GERAL', 'PONTOS-CHAVE', 'PRINCIPAIS LIÇÕES'],
                'detail': "Equilíbrio entre concisão e completude"
            },
            'longo': {
                'length': "300-400 palavras",
                'sections': ['VISÃO GERAL', 'PONTOS-CHAVE', 'PRINCIPAIS LIÇÕES', 'CONTEXTO', 'APLICAÇÕES'],
                'detail': "Análise detalhada com exemplos"
            }
        }

        # Mapeamento de códigos para nomes completos (apenas para exibição)
        language_names = {
            'pt': 'Português de Portugal',
            'en': 'Inglês',
            'es': 'Espanhol',
            'fr': 'Francês',
            'de': 'Alemão'
        }
        
        # Garante minúsculas e fallback para português
        target_code = targetLanguage.lower()
        if target_code not in language_mapping:
            target_code = 'pt'
        
        lang_data = language_mapping[target_code]
        type_rules = length_rules.get(summary_type.lower(), length_rules['normal'])
        
        # Filtro de secções
        lang_data['sections'] = [sec for sec in lang_data['sections'] 
                                if sec in type_rules.get('sections', [])]
        
        instruction = lang_data['instruction'].format(summary_type=summary_type)

        prompt_parts = [
            f"✨ {instruction}\n\n",
            f"🎯 {lang_data['title']}: [Crie um título claro e descritivo]\n\n",
            "".join([f"📌 {section}:\n- [Desenvolva esta seção]\n" for section in lang_data['sections']]),
            "\n📝 **Regras específicas para {summary_type}**:\n".format(summary_type=summary_type),
            f"- Extensão: {type_rules['length']}\n",
            f"- Nível de detalhe: {type_rules['detail']}\n",
            f"- Idioma: {language_names.get(target_code, 'Português')}\n",
            "- Formato:\n",
            "  * Títulos em negrito\n",
            "  * Marcadores para listas\n",
            "  * Parágrafos curtos\n\n",
            f"✂️ **Texto para resumir**:\n{text}\n\n",
            "🛑 **IMPORTANTE**:\n",
            "- Mantenha EXATAMENTE esta estrutura\n",
            "- Use apenas informações do texto fornecido\n",
            f"- Adapte a complexidade ao formato {summary_type}"
        ]

        return "".join(prompt_parts)

    @staticmethod
    def createTimestampPrompt(text: str, video_id: str, targetLanguage: str) -> str:
        """Gera prompt para timestamps usando códigos de idioma"""
        topic_words = {
            'pt': 'Tópico',
            'en': 'Topic',
            'es': 'Tema',
            'fr': 'Sujet',
            'de': 'Thema'
        }
        
        language_names = {
            'pt': 'PORTUGUÊS',
            'en': 'INGLÊS',
            'es': 'ESPANHOL',
            'fr': 'FRANCÊS',
            'de': 'ALEMÃO'
        }
        
        # Fallback para português
        target_code = targetLanguage.lower()
        if target_code not in topic_words:
            target_code = 'pt'
        
        topic_word = topic_words[target_code]
        lang_name = language_names.get(target_code, 'PORTUGUÊS')

        return f"""⏱️ GERAR TIMESTAMPS EM {lang_name}:

        Formato EXATO requerido:
        1. [hh:mm:ss] {topic_word} 1: [Título claro]
        2. [hh:mm:ss] {topic_word} 2: [Título claro]

        Regras absolutas:
        1. Use SOMENTE marcação [hh:mm:ss]
        2. Converta os tempos para formato 24h
        3. Liste 5-10 tópicos principais
        4. Títulos devem ser autoexplicativos
        5. NÃO inclua links ou segundos explicitamente

        Exemplo correto:
        [00:05:30] {topic_word} 1: Introdução

        Conteúdo para análise:
        {text}"""

    @staticmethod
    def createTranscriptPrompt(text: str, targetLanguage: str) -> str:
        language_instructions = {
            'de': "TRADUZA ESTE TEXTO PARA ALEMÃO (DEUTSCH) SEGUINDO ESTAS REGRAS RIGOROSAMENTE:",
            'fr': "TRADUISEZ CE TEXTE EN FRANÇAIS EN SUIVANT STRICTEMENT CES RÈGLES:",
            'es': "TRADUCE ESTE TEXTO AL ESPAÑOL SIGUIENDO ESTRICTAMENTE ESTAS REGLAS:",
            'en': "TRANSLATE THIS TEXT TO ENGLISH FOLLOWING THESE RULES STRICTLY:",
            'pt': "TRADUZA ESTE TEXTO PARA PORTUGUÊS DE PORTUGAL SEGUINDO ESTAS REGRAS RIGOROSAMENTE:"
        }
        
        # Fallback para instrução genérica
        instruction = language_instructions.get(targetLanguage, 
            f"TRANSLATE THIS TEXT TO {targetLanguage.upper()} FOLLOWING THESE RULES STRICTLY:")
        
        return f"""✨ {instruction}

        1. REMOVA QUALQUER MENÇÃO SOBRE:
        - Falta de marcadores de tempo
        - Suposições sobre blocos de tempo

        2. PRESERVE:
        - Termos técnicos entre *asteriscos*
        - Nomes próprios
        - Emoções do original

        3. ESPECIFICAÇÕES PARA O IDIOMA ALVO:
        - Use exclusivamente {targetLanguage.upper()}
        - Adapte expressões idiomáticas
        - Mantenha formalidade adequada
        - Siga as normas gramaticais do idioma

        4. NÃO COMENTE, APENAS TRADUZA!

        5. INÍCIE DIRETAMENTE COM A TRADUÇÃO:

        {text}"""