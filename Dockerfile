# Base Python
FROM python:3.11-slim

# Evita prompts de instalação interativa
ENV DEBIAN_FRONTEND=noninteractive
ENV PORT=8080

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y ffmpeg curl wget git && \
    rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia todo o projeto
COPY . /app

# Atualiza pip e instala dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta correta para o Koyeb
EXPOSE 8080

# Comando para iniciar o FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]