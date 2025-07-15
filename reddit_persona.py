import os
import re
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
CLAUDE_MODEL = "anthropic/claude-3-haiku"


def extract_username_from_url(url):
    match = re.search(r"reddit\.com/user/([^/]+)/?", url)
    return match.group(1) if match else None


def fetch_reddit_user_activity(username, max_items=10):
    headers = {'User-Agent': 'Mozilla/5.0'}
    urls = [
        f"https://www.reddit.com/user/{username}/comments/",
        f"https://www.reddit.com/user/{username}/overview/"
    ]

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            comment_divs = soup.find_all('div', class_='md', limit=max_items)
            comments = [div.get_text(strip=True) for div in comment_divs]
            if comments:
                return "\n".join(comments)
        except requests.RequestException as e:
            print(f"⚠️ Error fetching from {url}: {e}")

    return None


def fetch_user_avatar(username):
    url = f"https://www.reddit.com/user/{username}/about.json"
    headers = {"User-Agent": "persona-generator/0.1"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json().get("data", {})
        return data.get("icon_img") or data.get("subreddit", {}).get("icon_img")
    except Exception as e:
        print(f"⚠️ Error fetching avatar: {e}")
        return None


def score_to_class(score):
    if score >= 90:
        return "full"
    elif score >= 75:
        return "three-quarter"
    elif score >= 50:
        return "two-third"
    elif score >= 33:
        return "half"
    elif score >= 20:
        return "third"
    return "minimal"


def get_personality_from_claude(activity):
    prompt = f"""
You are an expert behavioral analyst. Given this Reddit user's activity, infer:

1. Personality across 4 Myers-Briggs dimensions.
2. Motivations based on observed behavior.
3. Key interests — returned as short tags.

Return ONLY this JSON structure (no explanation, no markdown, no extra content):

{{
  "personality": [
    {{ "dimension": "Introvert-Extrovert", "score": 65 }},
    {{ "dimension": "Intuition-Sensing", "score": 95 }},
    {{ "dimension": "Feeling-Thinking", "score": 80 }},
    {{ "dimension": "Perceiving-Judging", "score": 30 }}
  ],
  "motivations": [
    {{ "name": "Convenience", "score": 90 }},
    {{ "name": "Wellness", "score": 95 }},
    {{ "name": "Speed", "score": 80 }},
    {{ "name": "Preferences", "score": 50 }},
    {{ "name": "Comfort", "score": 30 }},
    {{ "name": "Dietary Needs", "score": 100 }}
  ],
  "interests": ["Politics", "Tech", "Fitness"]
}}

Reddit User Activity:
\"\"\"{activity}\"\"\"
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": CLAUDE_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a JSON-only analyst."},
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=30
        )

        content = response.json()["choices"][0]["message"]["content"]
        json_text = content[content.find("{"): content.rfind("}") + 1]
        parsed = json.loads(json_text)

        personality = [
            {
                "dimension": item["dimension"],
                "score": item["score"],
                "bar_class": score_to_class(item["score"])
            }
            for item in parsed.get("personality", [])
        ]

        motivations = [
            {
                "name": item["name"],
                "score": item["score"],
                "bar_class": score_to_class(item["score"])
            }
            for item in parsed.get("motivations", [])
        ]

        return personality, motivations

    except Exception as e:
        print("❌ Error parsing Claude response:", e)
        return [], []


def main():
    if not OPENROUTER_API_KEY:
        print("❌ Missing API key. Please add OPENROUTER_API_KEY in your .env file.")
        return

    url = input("Enter Reddit profile URL: ").strip()
    username = extract_username_from_url(url)
    if not username:
        print("❌ Invalid Reddit URL format.")
        return

    print(f"Fetching Reddit activity for: {username}")
    activity = fetch_reddit_user_activity(username)
    if not activity:
        print("❌ No activity found or error occurred.")
        return

    personality, motivations = get_personality_from_claude(activity)

    print("\n--- Persona Report ---")
    if personality:
        print("Personality Traits:")
        for item in personality:
            print(f"• {item['dimension']}: {item['score']} ({item['bar_class']})")
    else:
        print("⚠️ No personality data extracted.")

    if motivations:
        print("\nMotivations:")
        for item in motivations:
            print(f"• {item['name']}: {item['score']} ({item['bar_class']})")
    else:
        print("⚠️ No motivation data extracted.")

    output_path = f"{username}_persona.json"
    with open(output_path, "w") as f:
        json.dump({"personality": personality, "motivations": motivations}, f, indent=2)

    print(f"✅ Persona saved as {output_path}")


if __name__ == "__main__":
    main()
