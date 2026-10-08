from urllib.parse import urlparse, parse_qs
import re
import requests
import subprocess
from pathlib import Path
import json


def extract_video_id(url):
    parsed = urlparse(url)

    if parsed.hostname in ("youtu.be", "www.youtu.be"):
        return parsed.path.strip("/")

    if parsed.hostname in ("youtube.com", "www.youtube.com", "m.youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]

        match = re.match(r"/(?:shorts|embed)/([^/?]+)", parsed.path)
        if match:
            return match.group(1)

    return None


def inspect(url):
    video_id = extract_video_id(url)

    if not video_id:
        return {"error": "Could not extract a YouTube video ID."}

    canonical_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        response = requests.get(
            canonical_url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )

        page = response.text

        data = {
            "video_id": video_id,
            "url": canonical_url,
            "status_code": response.status_code,
            "title": None,
            "channel": None,
            "channel_url": None,
            "description": None,
            "published": None,
            "thumbnail": None,
        }

        # JSON-LD
        jsonld = re.findall(
            r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            page,
            re.I | re.S,
        )

        for block in jsonld:
            try:
                obj = json.loads(html.unescape(block.strip()))

                if isinstance(obj, dict):
                    data["title"] = data["title"] or obj.get("name")
                    data["description"] = data["description"] or obj.get("description")
                    data["thumbnail"] = data["thumbnail"] or (
                        obj.get("thumbnailUrl")[0]
                        if isinstance(obj.get("thumbnailUrl"), list)
                        and obj.get("thumbnailUrl")
                        else obj.get("thumbnailUrl")
                    )
                    data["published"] = data["published"] or obj.get("uploadDate")

                    author = obj.get("author")
                    if isinstance(author, dict):
                        data["channel"] = data["channel"] or author.get("name")
                        data["channel_url"] = data["channel_url"] or author.get("url")

            except Exception:
                pass

        # ytInitialPlayerResponse
        match = re.search(
            r'var ytInitialPlayerResponse\s*=\s*(\{.*?\});',
            page,
            re.S,
        )

        if match:
            try:
                player = json.loads(match.group(1))
                details = player.get("videoDetails", {})

                data["title"] = data["title"] or details.get("title")
                data["channel"] = data["channel"] or details.get("author")
                data["description"] = data["description"] or details.get("shortDescription")

                thumbs = details.get("thumbnail", {}).get("thumbnails", [])
                if thumbs:
                    data["thumbnail"] = data["thumbnail"] or thumbs[-1].get("url")

            except Exception:
                pass

        return data

    except requests.RequestException as error:
        return {
            "video_id": video_id,
            "error": str(error),
        }

def download(url, mode="mp4", output_dir=None):
    if output_dir is None:
        output_dir = Path.home() / "storage" / "downloads" / "TraceKit"

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if mode == "mp3":
        format_args = [
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
        ]
    else:
        format_args = [
            "-f", "bv*+ba/b",
            "--merge-output-format", "mp4",
        ]

    command = [
        "yt-dlp",
        *format_args,
        "-o", str(output_dir / "%(title)s.%(ext)s"),
        url,
    ]

    return subprocess.run(command).returncode

def print_result(result):
    print()

    if "error" in result:
        print("[ERROR]")
        print(f"  {result["error"]}")
        return

    print("[YOUTUBE OSINT]")
    print(f"Video ID:      {result["video_id"]}")
    print(f"Title:         {result.get("title") or "Unknown"}")
    print(f"Description:   {result.get("description") or "Unknown"}")
    print(f"Thumbnail:     {result.get("thumbnail") or "Unknown"}")
    print(f"Canonical URL: {result.get("canonical_url") or result.get("url")}")
    print(f"HTTP Status:   {result["status_code"]}")
