from fastapi import FastAPI, HTTPException
from yt_dlp import YoutubeDL

app = FastAPI()

@app.get("/pornhub")
async def get_video(url: str):
    ydl_opts = {"quiet": True, "nocheckcertificate": True}
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get("url")
        if not video_url:
            raise HTTPException(status_code=404, detail="Vídeo não encontrado")
        return {"status": 200, "video": video_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))