from flask import Flask, render_template, request, session, jsonify
from typing import Dict

from flask import Flask
import os
from dotenv import load_dotenv
from .chat.chat import ChatSession
import openai

load_dotenv()
app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')
app.secret_key = os.getenv("CHAT_APP_SECRET_KEY")


chat_sessions: Dict[str, ChatSession] = {}

@app.route("/")
def index():
    chat_session = _get_user_session()
    return render_template("chat.html", conversation=chat_session.get_messages())

# @app.route('/chat', methods=['POST'])
# def chat():
#     print("Chat endpoint called") # Debug line
#     message: str = request.json['message']
#     print("User message:", message) # Debug line
#     chat_session = _get_user_session()
#     chatgpt_message = chat_session.get_chatgpt_response(message)
#     return jsonify({"message": chatgpt_message})

@app.route('/chat', methods=['POST'])
def chat_endpoint():  # Rename this to avoid conflicts
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(f"Client IP Address: {client_ip}")
    print("Chat endpoint called")
    message: str = request.json['message']
    print("User message:", message)
    chat_session = _get_user_session()
    chatgpt_message = chat_session.get_chatgpt_response(message)
    return jsonify({"message": chatgpt_message})
    user_agent = request.headers.get('User-Agent')
    print(f"User-Agent: {user_agent}")
    cookies = request.cookies
    print(f"Cookies: {cookies}")
    session_data = session.get("some_key")
    print(f"Session data: {session_data}")

def _get_user_session() -> ChatSession:
    chat_session_id = session.get("chat_session_id")
    if chat_session_id:
        chat_session = chat_sessions.get(chat_session_id)
        if not chat_session:
            chat_session = ChatSession()
            chat_sessions[chat_session.session_id] = chat_session
            session["chat_session_id"] = chat_session.session_id
    else:
        chat_session = ChatSession()
        chat_sessions[chat_session.session_id] = chat_session
        session["chat_session_id"] = chat_session.session_id
    return chat_session
