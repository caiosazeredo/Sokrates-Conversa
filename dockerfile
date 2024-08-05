# Use uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto dos arquivos do projeto para o container
COPY . .

# Expõe a porta que o Flask vai usar
EXPOSE 5000

# Define a variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Comando para rodar a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]