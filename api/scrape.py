import requests
from bs4 import BeautifulSoup
import json

def handler(request):
    username = request.query.get("username")

    if not username:
        return {
            "status": 400,
            "body": json.dumps({"error": "username required"})
        }

    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.instagram.com/"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {
            "status": 500,
            "body": json.dumps({"error": "failed to fetch profile"})
        }
    
    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", type="application/ld+json")

    if not script_tag:
        return {
            "status": 500,
            "body": json.dumps({"error": "profile json not found"})
        }

    data = json.loads(script_tag.string)

    profile = {
        "username": data["author"]["name"],
        "bio": data["description"],
        "follower_count": data["author"]["interactionStatistic"][0]["userInteractionCount"],
        "post_count": data["author"]["interactionStatistic"][1]["userInteractionCount"]
    }

    return {
        "status": 200,
        "body": json.dumps(profile)
    }
