from yt_dlp import YoutubeDL
from pathlib import Path


def download_video(url, output_path=Path):
    output_path.mkdir(parents=True, exist_ok=True)
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "paths": {"home": str(output_path)},
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url, output_path):
    output_path.mkdir(parents=True, exist_ok=True)
    ydl_opts = {
        "format": "bestaudio/best",
        "paths": {"home": str(output_path)},
        "restrictfilenames": True,
        "remote_components": ["ejs:github"],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "0",
            }
        ],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=ogqeb9TLO8A"
    output_path = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
    download_audio(url, output_path)