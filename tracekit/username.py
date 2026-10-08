import requests


PLATFORMS = {
    "github": "https://github.com/{username}",
    "reddit": "https://www.reddit.com/user/{username}",
    "x": "https://x.com/{username}",
    "instagram": "https://www.instagram.com/{username}/",
}


def detect_status(platform, response):
    if response.status_code == 404:
        return False

    if response.status_code != 200:
        return None

    text = response.text.lower()

    if platform == "github":
        return True

    if platform == "reddit":
        if "this account has been suspended" in text:
            return False
        if "page not found" in text:
            return False
        return True

    if platform == "x":
        if "doesn't exist" in text or "account suspended" in text:
            return False
        return True

    if platform == "instagram":
        if "page isn't available" in text:
            return False
        return True

    return None


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
                "exists": detect_status(platform, response),
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
        exists = data.get("exists")

        if exists is True:
            state = "FOUND"
        elif exists is False:
            state = "NOT FOUND"
        else:
            state = "UNKNOWN"

        print(f"{platform:<12} {state:<10} HTTP: {status}")
