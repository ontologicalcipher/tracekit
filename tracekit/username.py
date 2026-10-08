import requests


PLATFORMS = {
    "github": "https://github.com/{username}",
    "reddit": "https://www.reddit.com/user/{username}",
    "x": "https://x.com/{username}",
    "instagram": "https://www.instagram.com/{username}/",
}


def check_username(username):
    results = {}

    headers = {
        "User-Agent": "TraceKit/1.0 (public username checker)"
    }

    for platform, template in PLATFORMS.items():
        url = template.format(username=username)

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=10,
                allow_redirects=True,
            )

            results[platform] = {
                "url": url,
                "status_code": response.status_code,
                "exists": response.status_code == 200,
            }

        except requests.RequestException as error:
            results[platform] = {
                "url": url,
                "error": str(error),
                "exists": None,
            }

    return {
        "username": username,
        "results": results,
    }


def print_result(result):
    print()
    print("[USERNAME OSINT]")
    print(f"Username: {result['username']}")
    print()

    for platform, data in result["results"].items():
        status = data.get("status_code", "ERROR")

        if data.get("exists") is True:
            state = "FOUND"
        elif data.get("exists") is False:
            state = "NOT FOUND"
        else:
            state = "UNKNOWN"

        print(f"{platform:<12} {state:<10} HTTP: {status}")
