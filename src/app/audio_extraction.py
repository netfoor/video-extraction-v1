import whisperx
import os
import json

from dotenv import load_dotenv

load_dotenv()

device = "cpu"
audio_file = "/workspace/data/raw/cut_audio.wav"

# Load model
model = whisperx.load_model(
    "small",
    device=device,
    compute_type="int8"
)

audio = whisperx.load_audio(audio_file)

# Transcribe
result = model.transcribe(audio)

print("\nTRANSCRIPTION:\n")

for segment in result["segments"]:
    print(segment["text"])

# Alignment
model_a, metadata = whisperx.load_align_model(
    language_code=result["language"],
    device=device
)

result = whisperx.align(
    result["segments"],
    model_a,
    metadata,
    audio,
    device
)

# Modern diarization import
from whisperx.diarize import DiarizationPipeline

diarize_model = DiarizationPipeline(
    token=os.getenv("HFACE"),
    device=device
)

diarize_segments = diarize_model(audio)

result = whisperx.assign_word_speakers(
    diarize_segments,
    result
)

print("\nFINAL RESULT:\n")

clean_segments = []

for segment in result["segments"]:
    speaker = segment.get("speaker", "UNKNOWN")
    text = segment["text"]

    print(f"{speaker}: {text}")

    clean_segments.append({
        "speaker": speaker,
        "start": segment["start"],
        "end": segment["end"],
        "text": text
    })

# Save JSON
output_path = "/workspace/data/processed/transcription.json"

os.makedirs(
    "/workspace/data/processed",
    exist_ok=True
)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(clean_segments, f, indent=2, ensure_ascii=False)

print(f"\nSaved to: {output_path}")