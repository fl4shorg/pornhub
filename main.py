from fastapi import FastAPI, HTTPException
from yt_dlp import YoutubeDL

app = FastAPI(title="FastAPI Multi-Platform Video Info API")

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Endpoint para obter informações do vídeo
@app.get("/video_info")
async def video_info(url: str, platform: str):
    # Configuração do yt-dlp
    ydl_opts = {
        "quiet": True,
        "nocheckcertificate": True,
        "skip_download": True,  # Não baixa, só extrai info
        "format": "best"         # Melhor qualidade disponível
    }

    # Plataformas válidas
    valid_platforms = ["pornhub", "kwai", "tiktok", "instagram"]
    if platform.lower() not in valid_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Plataforma inválida. Escolha: {valid_platforms}"
        )

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # Pega melhor vídeo disponível
        formats = info.get("formats", [])
        if not formats:
            raise HTTPException(status_code=404, detail="Nenhum formato de vídeo encontrado")

        best_format = max(formats, key=lambda f: f.get("height", 0))
        video_url = best_format.get("url")

        if not video_url:
            raise HTTPException(status_code=404, detail="Link de download não encontrado")

        # Retorna informações principais + thumbnail/capa
        response = {
            "status": 200,
            "platform": platform.lower(),
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
        raise HTTPException(status_code=500, detail=str(e))