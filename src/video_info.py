import os
import re
import tempfile
from bs4 import BeautifulSoup
import requests
from langdetect import detect, DetectorFactory
from yt_dlp import YoutubeDL

class GetVideo:
    @staticmethod
    def extract_video_id(youtube_url: str) -> str:
        patterns = [
            r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
            r"(?:embed\/)([0-9A-Za-z_-]{11})",
            r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})",
            r"(?:shorts\/)([0-9A-Za-z_-]{11})",
            r"^([0-9A-Za-z_-]{11})$"
        ]
        youtube_url = youtube_url.strip()
        for pattern in patterns:
            match = re.search(pattern, youtube_url)
            if match:
                return match.group(1)
        raise ValueError("Não foi possível extrair o ID do vídeo do URL")

    @staticmethod
    def title(link):
        try:
            r = requests.get(link)
            s = BeautifulSoup(r.text, "html.parser")
            title = s.find("meta", itemprop="name")["content"]
            return title
        except Exception:
            return "⚠️ Título não disponível ou link inválido."

    @staticmethod
    def _download_subtitles(video_url: str, lang: str = 'en') -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': [lang],
                'skip_download': True,
                'subtitlesformat': 'vtt',
                'outtmpl': os.path.join(tmpdir, '%(id)s.%(ext)s'),
                'quiet': True,
                'paths': {'home': tmpdir}
            }

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=True)
                    video_id = info_dict.get("id", None)

                if not video_id:
                    print("❌ ID do vídeo não encontrado.")
                    return None

                vtt_file = os.path.join(tmpdir, f"{video_id}.{lang}.vtt")
                if os.path.exists(vtt_file):
                    with open(vtt_file, 'r', encoding='utf-8') as f:
                        return f.read()
                else:
                    print("❌ Ficheiro VTT não encontrado.")
                    return None
            except Exception as e:
                print(f"❌ Erro ao usar yt_dlp: {e}")
                return None

    @staticmethod
    def limpar_vtt(vtt_text: str) -> str:
        linhas = vtt_text.splitlines()
        texto_sem_ruido = []
        for linha in linhas:
            linha = linha.strip()
            if (
                not linha or
                linha.startswith(('WEBVTT', 'Kind:', 'Language:', 'NOTE')) or
                re.match(r"\d{2}:\d{2}:\d{2}\.\d{3} -->", linha)
            ):
                continue
            linha = re.sub(r'</?c>', '', linha)
            linha = re.sub(r'align:\S+ position:\S+', '', linha)
            linha = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', linha)
            linha = linha.strip()
            if linha:
                texto_sem_ruido.append(linha)

        texto_final = []
        anterior = ""
        for linha in texto_sem_ruido:
            if linha != anterior:
                texto_final.append(linha)
                anterior = linha

        return ' '.join(texto_final)

    @staticmethod
    def transcript(link, fallback_language='en'):
        raw_vtt = GetVideo._download_subtitles(link, fallback_language)
        if not raw_vtt:
            return None
        return GetVideo.limpar_vtt(raw_vtt)

    @staticmethod
    def transcript_time(link, fallback_language='en'):
        raw_vtt = GetVideo._download_subtitles(link, fallback_language)
        if not raw_vtt:
            return None

        lines = raw_vtt.splitlines()
        transcript = []
        time = None
        for line in lines:
            if re.match(r"\d{2}:\d{2}:\d{2}\.\d{3} -->", line):
                time = line.split(' -->')[0].split('.')[0]
            elif line.strip() and time:
                transcript.append(f'{line.strip()} "time:{time}"')
                time = None
        return ' '.join(transcript)

    @staticmethod
    def detect_language(text):
        if not text:
            return 'en'
        try:
            DetectorFactory.seed = 0
            lang = detect(text)
            return {
                'pt': 'pt', 'en': 'en', 'es': 'es',
                'fr': 'fr', 'de': 'de', 'it': 'it',
                'nl': 'nl', 'ru': 'ru'
            }.get(lang, 'en')
        except:
            return 'en'
