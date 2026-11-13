# video-extraction-v1

Baseline pipeline that downloads the audio of a YouTube video and turns it into a speaker-labeled transcript with WhisperX. It was built to measure this first approach against others before choosing one.

## Features

- Downloads the best available audio from a YouTube URL and converts it to WAV (`yt-dlp` + FFmpeg)
- Cuts a time range out of the audio to keep test runs short
- Transcribes with WhisperX, aligns words and assigns a speaker to each segment (diarization)
- Saves the result as JSON: speaker, start, end and text per segment

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Speech to text | WhisperX (`small` model, CPU, `int8`) |
| Download | yt-dlp, FFmpeg |
| Environment | Docker (dev container), uv |

## Requirements

- Docker with Compose
- A Hugging Face access token, used by the diarization step

## Setup and usage

```bash
git clone https://github.com/netfoor/video-extraction-v1.git
cd video-extraction-v1
cp .env.example .env   # set HFACE to your Hugging Face token
docker compose -f docker-compose.dev.yml up -d --build
```

Then run the three steps inside the container (`dev-env`):

```bash
# 1. Download the audio to data/raw/
docker compose -f docker-compose.dev.yml exec dev-env uv run python src/app/download.py

# 2. Cut the part you want to test (edit the paths and times in the file first)
docker compose -f docker-compose.dev.yml exec dev-env uv run python src/app/cut_audio.py

# 3. Transcribe, align and diarize
docker compose -f docker-compose.dev.yml exec dev-env uv run python src/app/audio_extraction.py
```

The result is written to `data/processed/transcription.json`:

```json
[
  { "speaker": "SPEAKER_00", "start": 1.634, "end": 30.001, "text": "..." }
]
```

## Notes

- The URL, the file names and the cut range are hard-coded in each script, and the scripts expect the `/workspace` path of the dev container.
- `main.py` is only a placeholder.
- `data/processed/transcription.json` is a sample output.

## Status

Active. Personal project (May 2026), first iteration of a comparison between approaches.

## License

MIT
