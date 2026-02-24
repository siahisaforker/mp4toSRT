# generate_captions

Simple command-line tool to auto-generate captions (SRT) for video/audio files using OpenAI Whisper.

## Requirements

- Python 3.8+
- `ffmpeg` available on PATH (Whisper uses it to read media)

## Installation

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

If you previously installed the wrong `whisper` package, run:

```bash
pip uninstall -y whisper
pip install -U openai-whisper
```

### Windows PyTorch note

On Windows you may need to install PyTorch separately. For a CPU-only install run:

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

If you have CUDA, follow the official PyTorch instructions at https://pytorch.org to install the appropriate CUDA build.

## Usage

Basic usage (single file):

```powershell
python generate_captions.py "path\to\video.mp4"
```

Process a directory (recurses):

```powershell
python generate_captions.py "path\to\folder"
```

## Options

- `-m, --model` — Whisper model (tiny, base, small, medium, large). Default: `small`.
- `-l, --language` — Language code (e.g. `en`). If omitted, Whisper will auto-detect.
- `-o, --outdir` — Output directory for generated `.srt` files.

## Notes

- Transcription is compute-intensive; use smaller models for faster CPU runs.
- On CPU you may see the warning: "FP16 is not supported on CPU; using FP32 instead", this is expected behavior.
- To speed up transcription, use a GPU-enabled PyTorch build (see PyTorch install instructions).

---

Small note: I made this for my Jellyfin server and decided to make it public.
