import argparse
import json

from tracekit import __version__
from tracekit.domain import resolve, print_result
from tracekit.web import inspect, print_result as print_web_result
from tracekit.youtube import inspect as youtube_inspect, print_result as print_youtube_result, download as youtube_download


def main():
    parser = argparse.ArgumentParser(
        prog="tracekit",
        description="TraceKit - lightweight public-data OSINT toolkit",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"TraceKit {__version__}",
    )

    sub = parser.add_subparsers(dest="command")

    domain_parser = sub.add_parser(
        "domain",
        help="Gather public DNS information",
    )
    domain_parser.add_argument(
        "target",
        help="Domain name, e.g. example.com",
    )

    web_parser = sub.add_parser(
        "web",
        help="Inspect a public website",
    )
    web_parser.add_argument(
        "target",
        help="Website URL, e.g. https://example.com",
    )

    youtube_parser = sub.add_parser(
        "youtube",
        help="Inspect a public YouTube video",
    )
    youtube_parser.add_argument(
        "target",
        help="YouTube video URL",
    )
    youtube_parser.add_argument(
        "--mp3",
        action="store_true",
        help="Download audio as MP3",
    )
    youtube_parser.add_argument(
        "--mp4",
        action="store_true",
        help="Download video as MP4",
    )
    youtube_parser.add_argument(
        "--json",
        action="store_true",
        help="Output metadata as JSON",
    )
    sub.add_parser("username", help="Check a public username")
    sub.add_parser("metadata", help="Inspect local file metadata")

    args = parser.parse_args()

    if args.command == "web":
        result = inspect(args.target)
        print_web_result(result)
        return

    if args.command == "youtube":
        if args.mp3:
            print("[+] Downloading MP3...")
            youtube_download(args.target, "mp3")
            return

        if args.mp4:
            print("[+] Downloading MP4...")
            youtube_download(args.target, "mp4")
            return

        result = youtube_inspect(args.target)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_youtube_result(result)

        return

    if args.command == "domain":
        result = resolve(args.target)
        print_result(result)
        return

    if args.command:
        print(f"[+] Module selected: {args.command}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
