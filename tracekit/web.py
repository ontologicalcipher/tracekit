import requests


def inspect(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True,
            headers={
                "User-Agent": "TraceKit/0.1"
            },
        )

        return {
            "requested_url": url,
            "final_url": response.url,
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type", "Unknown"),
            "server": response.headers.get("server", "Unknown"),
            "content_length": response.headers.get("content-length", "Unknown"),
        }

    except requests.RequestException as error:
        return {
            "error": str(error)
        }


def print_result(result):
    print()

    if "error" in result:
        print("[ERROR]")
        print(f"  {result['error']}")
        return

    print(f"Requested URL: {result['requested_url']}")
    print(f"Final URL:     {result['final_url']}")
    print(f"Status:        {result['status_code']}")
    print(f"Content-Type:  {result['content_type']}")
    print(f"Server:        {result['server']}")
    print(f"Size:          {result['content_length']}")
