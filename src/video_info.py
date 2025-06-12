from youtube_transcript_api import YouTubeTranscriptApi 
from bs4 import BeautifulSoup
import requests
import re
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

class GetVideo:
    @staticmethod
    def extract_video_id(youtube_url: str) -> str:
        """Extracts the video ID from a YouTube video link."""
        patterns = [
            r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",      # URLs normais e partilhados
            r"(?:embed\/)([0-9A-Za-z_-]{11})",      # URLs embutidos
            r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})",  # URLs curtos
            r"(?:shorts\/)([0-9A-Za-z_-]{11})",     # YouTube Shorts
            r"^([0-9A-Za-z_-]{11})$"                # Apenas o ID
        ]
    
        youtube_url = youtube_url.strip()

        for pattern in patterns:
            match = re.search(pattern, youtube_url)
            if match:
                return match.group(1)
    
        raise ValueError("Não foi possível extrair o ID do vídeo do URL")
        
    @staticmethod
    def title(link):
        """Obter o titulo do video."""
        r = requests.get(link) 
        s = BeautifulSoup(r.text, "html.parser") 
        try:
            title = s.find("meta", itemprop="name")["content"]
            return title
        except TypeError:
            title = "⚠️ Parece haver um problema com o link do vídeo do YouTube fornecido. Por favor, verifique o link e tente novamente."
            return title
        
    @staticmethod
    def transcript(link, fallback_language='pt'):
        """Obtém transcrição com fallback inteligente"""
        video_id = GetVideo.extract_video_id(link)
        try:
            # Primeiro tenta no idioma padrão do vídeo
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=[fallback_language, 'en']  # Tenta primeiro no fallback, depois inglês
            )
            return " ".join(i['text'] for i in transcript)
        except:
            try:
                # Se falhar, tenta qualquer transcrição disponível
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                return " ".join(i['text'] for i in transcript)
            except Exception as e:
                print(f"Erro detalhado: {str(e)}")
                return None

    @staticmethod
    def transcript_time(link):
        """Obter a transcrição do video do Youtube com as timestamps."""
        video_id = GetVideo.extract_video_id(link)
        try:
            transcript_dict = YouTubeTranscriptApi.get_transcript(video_id)
            final_transcript = ""
            for i in transcript_dict:
                timevar = round(float(i["start"]))
                hours = int(timevar // 3600)
                timevar %= 3600
                minutes = int(timevar // 60)
                timevar %= 60
                timevex = f"{hours:02d}:{minutes:02d}:{timevar:02d}"
                final_transcript += f'{i["text"]} "time:{timevex}" '
            return final_transcript
        except Exception as e:
            print(e)
            return video_id
        
    @staticmethod
    def detect_language(text):
        """Detecção melhorada para múltiplos idiomas"""
        if not text:
            return 'en'  # Default para inglês
        
        try:
            DetectorFactory.seed = 0
            lang = detect(text)
            # Mapeamento simplificado
            return {
                'pt': 'pt',
                'en': 'en',
                'es': 'es',
                'fr': 'fr',
                'de': 'de',
                'it': 'it',
                'nl': 'nl',
                'ru': 'ru'
            }.get(lang, 'en')
        except:
            return 'en'