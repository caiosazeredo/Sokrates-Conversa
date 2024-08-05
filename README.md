# Sokrates-Conversa
 
1 - Crie um arquivo .env com o seguinte código:

GROQ_API_KEY=sua_chave_groq_aqui
GEMINI_API_KEY=sua_chave_gemini_aqui
OPENAI_API_KEY=sua_chave_openai_aqui

2- Para construir e rodar o container:

Sem docker-compose:
Copydocker build -t meu-chat-app .
docker run -p 5000:5000 --env-file .env meu-chat-app


Com docker-compose:
Copydocker-compose up --build
