from fastapi import FastAPI, HTTPException
from yt_dlp import YoutubeDL

app = FastAPI(title="FastAPI Multi-Platform Video Info API")

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Endpoint principal para extrair informações do vídeo
@app.get("/video_info")
async def video_info(url: str):
    """
    Recebe uma URL de vídeo (qualquer plataforma suportada pelo yt-dlp)
    e retorna:
    - download_url (melhor qualidade)
    - thumbnail
    - title, uploader, duration, description
    """
    # Configuração do yt-dlp
    ydl_opts = {
        "quiet": True,
        "nocheckcertificate": True,
        "skip_download": True,  # não baixa, só extrai info
        "format": "best"         # melhor qualidade disponível
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # Pega melhor vídeo disponível
        formats = info.get("formats", [])
        if not formats:
            raise HTTPException(status_code=404, detail="Nenhum formato de vídeo encontrado")

        # Seleciona o vídeo com maior resolução
        best_format = max(formats, key=lambda f: f.get("height", 0) or 0)
        video_url = best_format.get("url")
        if not video_url:
            raise HTTPException(status_code=404, detail="Link de download não encontrado")

        # Retorna JSON com informações principais
        response = {
            "status": 200,
            "platform": info.get("extractor_key", "desconhecida"),  # identifica a plataforma
            "title": info.get("title", "Indisponível"),
            "uploader": info.get("uploader", "Indisponível"),
            "upload_date": info.get("upload_date", "Indisponível"),
            "duration": info.get("duration", "Indisponível"),
            "description": info.get("description", "Indisponível"),
            "thumbnail": info.get("thumbnail", None),
            "download_url": video_url
        }

        return response

    except Exception as e:
        # Se yt-dlp não conseguir extrair o vídeo
        raise HTTPException(status_code=500, detail=str(e))