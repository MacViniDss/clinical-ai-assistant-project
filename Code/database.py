# database.py
import sqlite3
import uuid
from datetime import datetime

DB_NAME = "chat_history.db"

def get_connection():
    # check_same_thread=False é necessário para o Streamlit
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# Roda sempre que o app inicia para garantir que as tabelas sessions (os chats criadas) e messages (o conteúdo das conversas) existam.
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Tabela para gerenciar as sessões de chat
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            title TEXT,
            created_at TEXT
        )
    ''')
    # Tabela para guardar as mensagens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TEXT,
            FOREIGN KEY(session_id) REFERENCES sessions(session_id)
        )
    ''')
    conn.commit()
    conn.close()

# Gera um ID único (UUID) para um novo chat e salva no banco.
def create_session(title="Novo Chat"):
    session_id = str(uuid.uuid4())
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sessions (session_id, title, created_at) VALUES (?, ?, ?)', 
                   (session_id, title, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return session_id

# Busca todos os chats anteriores para listar na barra lateral do app.
def get_all_sessions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT session_id, title FROM sessions ORDER BY created_at DESC')
    sessions = cursor.fetchall()
    conn.close()
    return sessions

# Grava cada nova mensagem, identificando se foi o user ou o model (IA) que enviou.
def save_message(session_id, role, content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)',
                   (session_id, role, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# Recupera o histórico de uma sessão específica para reconstruir o contexto para o Gemini e para a tela.
def get_messages(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role, content FROM messages WHERE session_id = ? ORDER BY timestamp ASC', (session_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages