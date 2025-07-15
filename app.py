import os
import re
import json
import requests

from flask import Flask, render_template, request, redirect, url_for
from reddit_persona import (
    extract_username_from_url,
    fetch_reddit_user_activity,
    get_personality_from_claude,
    fetch_user_avatar,
)

app = Flask(__name__)


def score_to_class(score):
    if score >= 80:
        return "bar-high"
    elif score >= 50:
        return "bar-medium"
    return "bar-low"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        reddit_url = request.form.get("reddit_url")
        print(f"Processing {reddit_url}")

        username = extract_username_from_url(reddit_url)
        avatar_url = fetch_user_avatar(username)
        activity = fetch_reddit_user_activity(username)
        parsed = get_personality_from_claude(activity)

        print(f"\nFetched Reddit activity:\n{activity}\n")

        # Prompt for goals, frustrations, habits, and quote
        prompt_context = f"""
        You are a UX persona researcher.
        Based on this Reddit user's activity, return a valid JSON object with:
        quote, goals, frustrations, habits.
        Format:
        {{
          "quote": "...",
          "goals": ["..."],
          "frustrations": ["..."],
          "habits": ["..."]
        }}
        Guidelines:
        - Keep values short, readable, and natural
        - No bullets or markdown
        - Use only valid JSON
        Reddit Activity:
        \"\"\"{activity}\"\"\"
        """

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }

        payload_context = {
            "model": "anthropic/claude-3-haiku",
            "messages": [{"role": "user", "content": prompt_context}]
        }

        payload_core = {
            "model": "anthropic/claude-3-haiku",
            "messages": [
                {
                    "role": "user",
                    "content": f"""
You are an expert UX researcher. Analyze this Reddit activity and return valid JSON:
quote, age, occupation, status, location, tier, archetype, habits, frustrations, goals,
motivations, personality, interests.
Reddit Activity:
{activity}
                    """
                }
            ]
        }

        context_results = {}
        try:
            response_ctx = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload_context
            )
            content_ctx = response_ctx.json()["choices"][0]["message"]["content"]
            match_ctx = re.search(r"\{.*\}", content_ctx, re.DOTALL)
            context_results = json.loads(match_ctx.group()) if match_ctx else {}
        except Exception as e:
            print("Error from context prompt:", e)

        results = {}
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload_core
            )
            content = response.json()["choices"][0]["message"]["content"]
            match = re.search(r"\{.*\}", content, re.DOTALL)
            results = json.loads(match.group()) if match else {}

            # Clean interests if needed
            interests = results.get("interests", [])
            if isinstance(interests, str):
                rough_split = re.findall(r"[A-Z][a-z]+(?:\s?[a-z]+)*", interests)
                results["interests"] = [
                    s.strip().title() for s in rough_split if s.strip()
                ]

            print("Cleaned interests:", results.get("interests", []))
        except Exception as e:
            print("Error parsing Claude output:", e)

        # Merge results
        results = {**results, **context_results}
        results["username"] = username
        results["avatar_url"] = avatar_url

        # Sample hardcoded values (optional fallback)
        results["personality"] = [
            {"dimension": "Introvert vs Extrovert", "score": 45},
            {"dimension": "Intuition vs Sensing", "score": 70},
            {"dimension": "Feeling vs Thinking", "score": 65},
            {"dimension": "Perceiving vs Judging", "score": 60}
        ]

        results["motivations"] = [
            {"name": "Convenience", "score": 90},
            {"name": "Wellness", "score": 95},
            {"name": "Speed", "score": 80},
            {"name": "Preferences", "score": 50},
            {"name": "Comfort", "score": 30},
            {"name": "Dietary Needs", "score": 100}
        ]

        os.makedirs("output", exist_ok=True)
        with open("output/persona.json", "w") as f:
            json.dump(results, f, indent=4)

        return redirect(url_for("persona"))

    return render_template("index.html")


@app.route("/persona")
def persona():
    try:
        with open("output/persona.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        return f"Error loading persona.json: {e}"

    personality = [
        {
            "dimension": item.get("dimension", "-"),
            "score": item.get("score", 0),
            "score_class": score_to_class(item.get("score", 0))
        }
        for item in data.get("personality", [])
    ]

    motivations = [
        {
            "name": item.get("name", "-"),
            "score": item.get("score", 0),
            "score_class": score_to_class(item.get("score", 0))
        }
        for item in data.get("motivations", [])
    ]

    fallback_interests = ["Culture", "Technology", "Food"]
    interests = data.get("interests", [])[:]
    for item in fallback_interests:
        if len(interests) >= 3:
            break
        if item not in interests:
            interests.append(item)

    return render_template(
        "persona.html",
        username=data.get("username", "Unknown").title(),
        quote=data.get("quote", "No quote available."),
        age=data.get("age", "Unknown"),
        occupation=data.get("occupation", "Unknown"),
        relationship_status=data.get("status", "Unknown"),
        location=data.get("location", "Unknown"),
        adoption_tier=data.get("tier", "Unclassified"),
        user_archetype=data.get("archetype", "Undefined"),
        habits_and_behaviors=data.get("habits", []),
        frustrations=data.get("frustrations", []),
        goals_and_needs=data.get("goals", []),
        motivations=motivations,
        personality=personality,
        interests=interests,
        avatar_url=data.get("avatar_url")
    )


if __name__ == "__main__":
    app.run(debug=True)
