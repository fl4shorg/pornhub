from fastapi import FastAPI, HTTPException
from yt_dlp import YoutubeDL

app = FastAPI(title="FastAPI PornHub API")

@app.get("/pornhub")
async def get_video(url: str):
    # Configuração do yt-dlp
    ydl_opts = {
        "quiet": True,             # evita logs excessivos
        "nocheckcertificate": True,# ignora certificados SSL inválidos
        "skip_download": True      # não baixa o vídeo, só extrai info
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get("url")
            title = info.get("title", "Indisponível")

        if not video_url:
            raise HTTPException(status_code=404, detail="Vídeo não encontrado")

        return {
            "status": 200,
            "title": title,
            "video": video_url,
            "note": "API rodando no Leapcell serverless"
        }

    except Exception as e:
        # Se yt-dlp não conseguir extrair título ou link
        raise HTTPException(status_code=500, detail=str(e))