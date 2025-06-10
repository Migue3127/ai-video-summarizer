import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('resumos.db')
    c = conn.cursor()
    
    # Tabela de Utilizadores 
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 password TEXT)''')
    
    # Tabela de Histórico 
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 video_url TEXT,
                 video_title TEXT,
                 summary TEXT,
                 language TEXT,
                 detail_level TEXT,
                 created_at TIMESTAMP,
                 UNIQUE(user_id, video_url, language))''')
    
    # Tabela de Cache
    c.execute('''CREATE TABLE IF NOT EXISTS cache
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 video_id TEXT,
                 language TEXT,
                 detail_level TEXT,
                 summary TEXT,
                 created_at TIMESTAMP,
                 expires_at TIMESTAMP)''')
    
    # Tabela para cache de áudio
    c.execute('''CREATE TABLE IF NOT EXISTS cache_audio
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  text_hash TEXT UNIQUE,
                  audio_data TEXT,
                  lang_code TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  expires_at TIMESTAMP)''')
    
    
    conn.commit()
    conn.close()