import sqlite3
import hashlib
from gtts import gTTS
import io
import base64
import time
from datetime import datetime, timedelta

class TextToSpeech:
    # Configurações por idioma
    TTS_CONFIG = {
        'pt': {'tld': 'pt', 'lang': 'pt'},
        'en': {'tld': 'com', 'lang': 'en'},
        'es': {'tld': 'es', 'lang': 'es'},
        'fr': {'tld': 'fr', 'lang': 'fr'},
        'de': {'tld': 'de', 'lang': 'de'}
    }

    @staticmethod
    def get_audio(text: str, lang_code: str) -> bytes:
        """Obtém áudio do cache ou gera novo"""
        if not text.strip():
            return None
        
        text_hash = TextToSpeech._hash_text(text, lang_code)
        cached_audio = TextToSpeech._get_cached_audio(text_hash)
        
        if cached_audio:
            return base64.b64decode(cached_audio)
        
        return TextToSpeech._generate_and_cache_audio(text, lang_code, text_hash)

    @staticmethod
    def _hash_text(text: str, lang_code: str) -> str:
        """Gera hash único para texto + idioma"""
        return hashlib.sha256(f"{lang_code}-{text}".encode()).hexdigest()

    @staticmethod
    def _get_cached_audio(text_hash: str) -> bytes:
        """Busca áudio no cache do banco de dados"""
        conn = None
        try:
            conn = sqlite3.connect('resumos.db')
            c = conn.cursor()
            c.execute("SELECT audio_data FROM cache_audio WHERE text_hash=?", (text_hash,))
            result = c.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Erro ao buscar áudio em cache: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def _generate_and_cache_audio(text: str, lang_code: str, text_hash: str) -> bytes:
        """Gera novo áudio e salva no cache"""
        config = TextToSpeech.TTS_CONFIG.get(lang_code, TextToSpeech.TTS_CONFIG['pt'])
        
        try:
            tts = gTTS(text=text, lang=config['lang'], tld=config['tld'])
            with io.BytesIO() as buffer:
                tts.write_to_fp(buffer)
                buffer.seek(0)
                audio_bytes = buffer.read()
            
            TextToSpeech._save_to_cache(text_hash, audio_bytes, lang_code)
            return audio_bytes
        except Exception as e:
            print(f"Erro TTS: {e}")
            return None

    @staticmethod
    def _save_to_cache(text_hash: str, audio_data: bytes, lang_code: str):
        """Armazena áudio na base de dados"""
        conn = None
        try:
            audio_b64 = base64.b64encode(audio_data).decode('utf-8')
            expires_at = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
            conn = sqlite3.connect('resumos.db')
            c = conn.cursor()
            c.execute("""INSERT INTO cache_audio 
                         (text_hash, audio_data, lang_code, expires_at) 
                         VALUES (?, ?, ?, ?)""",
                      (text_hash, audio_b64, lang_code, expires_at))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  
        except sqlite3.Error as e:
            print(f"Erro ao salvar áudio em cache: {e}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def clear_expired_cache():
        """Remove entradas expiradas do cache"""
        conn = None
        try:
            conn = sqlite3.connect('resumos.db')
            c = conn.cursor()
            c.execute("DELETE FROM cache_audio WHERE expires_at < DATETIME('now')")
            deleted_count = c.rowcount
            conn.commit()
            print(f"Removidas {deleted_count} entradas expiradas do cache de áudio")
            return deleted_count
        except sqlite3.Error as e:
            print(f"Erro ao limpar cache expirado: {e}")
            return 0
        finally:
            if conn:
                conn.close()