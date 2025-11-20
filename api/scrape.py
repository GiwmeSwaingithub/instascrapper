import requests
from bs4 import BeautifulSoup
import json

def handler(request):
    username = request.query.get("username", "")

    if not username:
        return {
            "status": 400,
            "body": json.dumps({"error": "username is required"})
        }

    try:
        url = f"https://www.instagram.com/{username}/"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": "https://www.instagram.com/"
        }

        response = requests.get(url, headers=headers, timeout=10)

        # Instagram blocks datacenter IPs often (403/429)
        if response.status_code != 200:
            return {
                "status": 500,
                "body": json.dumps({"error": "Instagram blocked the request or user not found"})
            }

        soup = BeautifulSoup(response.text, "html.parser")

        script_tag = soup.find("script", type="application/ld+json")

        if not script_tag:
            return {
                "status": 500,
                "body": json.dumps({"error": "Instagram page structure changed or JSON not found"})
            }

        data = json.loads(script_tag.string)

        profile = {
            "username": data["author"]["name"],
            "bio": data.get("description", ""),
            "follower_count": data["author"]["interactionStatistic"][0]["userInteractionCount"],
            "post_count": data["author"]["interactionStatistic"][1]["userInteractionCount"]
        }

        return {
            "status": 200,
            "body": json.dumps(profile)
        }

    except Exception as err:
        return {
            "status": 500,
            "body": json.dumps({"error": str(err)})
        }
