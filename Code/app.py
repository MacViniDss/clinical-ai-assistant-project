import streamlit as st
import google.generativeai as genai
import os
import database as db
from dotenv import load_dotenv


# 1. Configuração da Página e Banco de Dados
st.set_page_config(page_title="Gemini ChatApp", layout="wide")
db.init_db()

# 2. Configuração da API do Gemini
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=API_KEY)


SYSTEM_PROMPT = """
Você é um médico renomado endocrinologista e trabalha em um hospital com muitos
pacientes.
Um deles é o seguinte paciente:
(dados do paciente fictício)
Forneça um plano de tratamento personalizado que inclua orientações dietéticas,
exercícios e monitoramento da glicose. Use linguagem simples.
Comece com uma breve introdução sobre a importância do tratamento adequado para
pacientes com diabetes e hipertensão.
Em seguida, forneça orientações específicas para a dieta do paciente, incluindo
recomendações sobre alimentos a serem evitados e alimentos benéficos.
Continue com diretrizes para a prática regular de exercícios físicos, detalhando os tipos
de exercícios, a frequência e a duração ideais.
Aborde o monitoramento da glicose, explicando como o paciente deve realizar os
testes, interpretar os resultados e agir de acordo com as leituras.
Detalhe a prescrição médica para o caso desse paciente.
Conclua com uma recapitulação das principais etapas do plano de tratamento e a
importância de seguir as recomendações.

"""

# Inicializando o modelo com o Prompt Engineering
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# 3. Gerenciamento de Estado da Sessão (Session State)
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

# 4. Interface: Sidebar para Histórico de Chats (Fase 2)
with st.sidebar:
    st.title("Histórico de Chats")
    
    # Formulário para criar chat com nome 
    with st.form(key="new_chat_form", clear_on_submit=True):
        new_chat_name = st.text_input(
            "Nome do Novo Chat:", 
            placeholder="Ex: Análise de Dados Financeiros"
        )
        submit_button = st.form_submit_button("Criar Chat", use_container_width=True)
        
        if submit_button:
            if new_chat_name.strip(): # Verifica se o usuário não deixou em branco
                # Chama a função passando o nome digitado
                st.session_state.current_session_id = db.create_session(title=new_chat_name.strip())
                st.rerun()
            else:
                # Aviso caso o usuário clique em criar sem digitar nada
                st.warning("Por favor, digite um nome para o chat.")

    st.divider()
    
    # Lista os chats existentes
    sessions = db.get_all_sessions()
    for session_id, title in sessions:
        if st.button(f"{title}", key=session_id, use_container_width=True):
            st.session_state.current_session_id = session_id
            st.rerun()

# 5. Interface: Área Principal do Chat (Fase 1)
if st.session_state.current_session_id is None:
    st.title("Bem-vindo ao WebApp do Gemini")
    st.write("Crie um **Novo Chat** na barra lateral para começar.")
else:
    current_session = st.session_state.current_session_id
    st.title("Conversa Atual")

    # Carregar mensagens do banco de dados (SQLite)
    chat_history = db.get_messages(current_session)
    
    # Reconstruir o histórico no objeto do Gemini para ele ter contexto da conversa
    gemini_history = []
    for role, content in chat_history:
        gemini_history.append({
            "role": "user" if role == "user" else "model",
            "parts": [content]
        })
    
    # Iniciar a sessão de chat do Gemini com o histórico recuperado
    chat = model.start_chat(history=gemini_history)

    # Exibir as mensagens na tela
    for role, content in chat_history:
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(content)

    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem para o Gemini..."):
        # Exibir a mensagem do usuário imediatamente
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Salvar a mensagem do usuário no DB
        db.save_message(current_session, "user", prompt)

        # Chamar a API do Gemini e obter a resposta
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = chat.send_message(prompt)
                st.markdown(response.text)
        
        # Salvar a resposta no DB
        db.save_message(current_session, "model", response.text)
