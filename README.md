# TraceKit

A lightweight command-line OSINT and public-data reconnaissance toolkit built with Python.

## Features

- Domain reconnaissance
- Web inspection
- YouTube metadata extraction
- YouTube media downloading through yt-dlp
- Modular Python architecture
- Designed for Termux/Linux environments

## Installation

```bash
git clone git@github.com:ontologicalcipher/tracekit.git
cd tracekit
pip install -r requirements.txt
```

## Usage

### Domain

```bash
python -m tracekit domain example.com
```

### Web

```bash
python -m tracekit web https://example.com
```

### YouTube metadata

```bash
python -m tracekit youtube "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download MP3

```bash
python -m tracekit youtube "https://www.youtube.com/watch?v=VIDEO_ID" --mp3
```

### Download MP4

```bash
python -m tracekit youtube "https://www.youtube.com/watch?v=VIDEO_ID" --mp4
```

Downloads are stored in `~/storage/downloads/TraceKit/`.

## Legal & Ethical Use

TraceKit is intended for legitimate OSINT, research, education, defensive security, and authorized investigations.

Only access or download data that you are legally permitted to access. Do not use TraceKit to bypass authentication, DRM, paywalls, access controls, or other security mechanisms.

## License

MIT License
