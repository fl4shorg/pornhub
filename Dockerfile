# Base Python
FROM python:3.11-slim

# Evita prompts interativos
ENV DEBIAN_FRONTEND=noninteractive
ENV PORT=8080

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y ffmpeg curl wget git libssl-dev libffi-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia o projeto para o container
COPY . /app

# Atualiza pip e yt-dlp
RUN pip install --upgrade pip
RUN pip install --upgrade yt-dlp
RUN pip install -r requirements.txt

# Expõe a porta que o Koyeb vai usar
EXPOSE 8080

# Comando para iniciar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]