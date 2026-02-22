#!/usr/bin/env python3
"""Simple CLI to auto-generate captions (SRT) for MP4 files using OpenAI Whisper."""
from pathlib import Path
import argparse
import datetime
import sys

def format_timestamp(seconds: float) -> str:
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    ms = int((td - datetime.timedelta(seconds=total_seconds)).total_seconds() * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"

def write_srt(segments, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for i, s in enumerate(segments, start=1):
            start = format_timestamp(s["start"])
            end = format_timestamp(s["end"])
            text = s.get("text", "").strip().replace("-->", "->")
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

def transcribe_file(path: Path, model_name: str, language: str, output_dir: Path):
    try:
        import whisper
    except Exception as e:
        print("Failed to import the 'whisper' package:", e)
        print()
        print("Common fixes:")
        print(" - You may have installed a different 'whisper' package. Run:")
        print("     pip uninstall -y whisper")
        print("     pip install -U openai-whisper")
        print()
        print(" - Whisper requires PyTorch. On Windows (CPU-only) run:")
        print("     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu")
        print()
        print("After installing the above, re-run this script.")
        sys.exit(1)

    print(f"Loading model '{model_name}' (this may take a while)...")
    model = whisper.load_model(model_name)
    kwargs = {}
    if language:
        kwargs["language"] = language

    print(f"Transcribing: {path}")
    result = model.transcribe(str(path), **kwargs)
    segments = result.get("segments", [])
    out_name = path.with_suffix("").name + ".srt"
    out_path = (output_dir or path.parent) / out_name
    write_srt(segments, out_path)
    print(f"Wrote captions: {out_path}")
    return out_path

def find_media_files(directory: Path):
    exts = {".mp4", ".m4v", ".mov", ".mkv", ".wav", ".mp3"}
    for p in directory.rglob("*"):
        if p.suffix.lower() in exts and p.is_file():
            yield p

def parse_args():
    p = argparse.ArgumentParser(description="Generate SRT captions for video/audio files using Whisper")
    p.add_argument("input", help="Input file or directory")
    p.add_argument("-m", "--model", default="small", help="Whisper model size (tiny, base, small, medium, large)")
    p.add_argument("-l", "--language", default=None, help="Language code (e.g., en). If omitted, Whisper will auto-detect")
    p.add_argument("-o", "--outdir", default=None, help="Output directory for generated .srt files")
    return p.parse_args()

def main():
    args = parse_args()
    inp = Path(args.input)
    outdir = Path(args.outdir) if args.outdir else None
    if inp.is_file():
        transcribe_file(inp, args.model, args.language, outdir)
    elif inp.is_dir():
        files = list(find_media_files(inp))
        if not files:
            print("No supported media files found in directory.")
            sys.exit(1)
        for f in files:
            transcribe_file(f, args.model, args.language, outdir)
    else:
        print("Input path not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
