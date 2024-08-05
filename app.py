from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
import google.generativeai as genai

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar a aplicação Flask
app = Flask(__name__)

# Obter chaves da API dos arquivos .env ou variáveis de ambiente
groq_api_key = os.getenv("GROQ_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Inicializar LLMs com as chaves da API
llm_llama = ChatGroq(temperature=0.7, model_name="llama3-70b-8192", groq_api_key=groq_api_key)
genai.configure(api_key=gemini_api_key)
gemini_model = genai.GenerativeModel('gemini-pro')
llm_gpt = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", api_key=openai_api_key)

# Criar memórias separadas para cada modelo
memories = {
    'llama': ConversationBufferMemory(memory_key="chat_history"),
    'gemini': ConversationBufferMemory(memory_key="chat_history"),
    'gpt': ConversationBufferMemory(memory_key="chat_history")
}

# Template para conversa generalista em português
prompt_template = PromptTemplate.from_template("""
Você é um agente conversacional amigável e conhecedor.
Engage-se em uma conversa natural e aberta com o usuário.

{chat_history}
Usuário: {input}
Agente:
""")

def generate_response(user_input, chat_history, model):
    if model == 'llama':
        prompt = prompt_template.format(chat_history=chat_history, input=user_input)
        response = llm_llama.invoke(prompt)
        return response.content
    elif model == 'gemini':
        full_prompt = f"{chat_history}\nUsuário: {user_input}\nAgente:"
        response = gemini_model.generate_content(full_prompt)
        return response.text
    elif model == 'gpt':
        prompt = prompt_template.format(chat_history=chat_history, input=user_input)
        response = llm_gpt.invoke(prompt)
        return response.content
    else:
        return "Modelo não suportado."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    model = request.form['model']
    
    chat_history = memories[model].buffer
    response_text = generate_response(user_message, chat_history, model)
    memories[model].save_context({"input": user_message}, {"output": response_text})
    
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)