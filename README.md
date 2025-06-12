VideoMind PRO - Resumos de Vídeos do YouTube com IA
==================================================

📌 Descrição do Projeto:
Aplicação web em Streamlit que utiliza a IA Google Gemini para gerar resumos inteligentes
de vídeos do YouTube em vários idiomas, com funcionalidade de texto-para-voz e
histórico de utilizador.

🌟 Funcionalidades Principais:
- Resumo automático por IA (Português, Inglês, Espanhol, Francês, Alemão)
- Três níveis de tamanhos: Curto, Padrão, Longo
- Geração de áudio dos resumos (TTS)
- Sistema de autenticação de utilizadores
- Sistema de cache inteligente
- Análise do vídeo com timestamps
- Tradução de transcrições

⚙️ Requisitos do Sistema:
- Python 3.7 ou superior
- Chave de API do Google Gemini
- Conexão à internet

📦 Guia de Instalação:
----------------------

1. Configuração Inicial:

   a) Descarregar os ficheiros do projeto para uma pasta local

   b) Criar e ativar ambiente virtual:
      # Windows:
      python -m venv venv
      venv\Scripts\activate
      
      # macOS/Linux:
      python3 -m venv venv
      source venv/bin/activate

2. Instalar Dependências:
   pip install -r requirements.txt

3. Configuração:
   Criar ficheiro .env na pasta principal com:
   GOOGLE_GEMINI_API_KEY=sua_chave_de_api_aqui

🚀 Executar a Aplicação:
------------------------
com o visual studio code aberto com o projeto executar: ctrl+shift+c (ira abrir a cmd já dentro da pasta do projeto)

EXECUTAR O COMANDO NA CMD:
streamlit run app.py

A aplicação irá abrir no navegador padrão em:
http://localhost:8501

🔧 Estrutura do Projeto:
-----------------------
/VideoMind-PRO
│   app.py                 - Ficheiro principal
│   requirements.txt       - Lista de dependências
│   .env                   - Modelo para configuração
│   README.txt             - Este ficheiro
│
├───src/
│   │   database.py        - Configuração da base de dados
│   │   model.py           - Integração com Gemini AI
│   │   prompt.py          - Construção de prompts para IA
│   │   tts.py             - Sistema de texto-para-voz
│   │   video_info.py      - Extração de dados do YouTube
│   │   translations.py    - Suporte a múltiplos idiomas
│   │   action_buttons.py  - Botões de ação na interface
│   │   misc.py            - Utilidades e CSS
│   │
│   ├───paginas/           - Páginas adicionais
│   │       tutorial.py
│   │       faq.py
│   │       privacidade.py
│
└───assets/                - Recursos visuais
        logo.png             - Logótipo da aplicação

💾 Informação sobre a Base de Dados:
-----------------------------------
A aplicação utiliza SQLite3 com criação automática da base de dados:
- Ficheiro: resumos.db
- Tabelas:
  * users (contas de utilizador)
  * history (histórico de resumos)
  * cache (sistema de cache)
  * cache_audio (cache de áudio TTS)
(o cache é eliminado após 7 dias)

⚠️ Resolução de Problemas:
-------------------------
1. Erros "No module named...":
   - Reinstalar dependências: pip install -r requirements.txt
   - Verificar versão do Python (3.7+ necessário)

2. Problemas com chave de API:
   - Verificar se o ficheiro .env está na pasta correta
   - Confirmar a chave em https://ai.google.dev/

3. Problemas com geração de áudio:
   - Verificar permissões de escrita na pasta
   - Confirmar instalação das dependências de áudio

4. Histórico
   - Após gerar um resumo, a parte do histórico só atualiza ao realizar alguma ação na barra lateral, como trocar o idioma, (nem que seja clicar no mesmo)

5. Erros de transcrição disponível
   - introduzir o link do vídeo de novo ou clicar gerar resumo até dar, (isto pode acontecer porque o YoutubeTranscriptApi não buscou corretamente a transcrição)

6. Cache
    - Como a base de dados guarda cache, para não haver calls desnecessárias à API, caso queira apagar este cache, é só apagar a base de dados visto que esta e criada automaticamente

📌 Notas Importantes:
- Manter as chaves de API em segurança
- A base de dados resumos.db será criada automaticamente
- Para uso prolongado, recomenda-se backup periódico da base de dados
