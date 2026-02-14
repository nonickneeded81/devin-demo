import sys
from datetime import datetime

import requests as http_client
from flask import Flask, jsonify, render_template, request

ACTORS = {
    "01-09": "Dave Bautista",
    "02-11": "Taylor Lautner",
    "03-26": "Robert Downey Jr.",
    "04-04": "Robert Downey Jr.",
    "05-25": "Cillian Murphy",
    "06-01": "Morgan Freeman",
    "07-09": "Tom Hanks",
    "08-19": "Matthew Perry",
    "09-02": "Keanu Reeves",
    "10-28": "Bill Gates (not actor, placeholder example)",
    "11-11": "Leonardo DiCaprio",
    "12-18": "Brad Pitt",
}

app = Flask(__name__)


def _search_wikipedia_births(month: str, day: str) -> str:
    url = f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/births/{month}/{day}"
    headers = {"User-Agent": "BirthdayActorMatcher/1.0"}
    try:
        resp = http_client.get(url, headers=headers, timeout=8)
        resp.raise_for_status()
        births = resp.json().get("births", [])
        for entry in births:
            desc = entry.get("text", "").lower()
            if "actor" in desc or "actress" in desc:
                return entry["text"]
        return "No matching actor found on Wikipedia either."
    except Exception:
        return "Could not reach Wikipedia right now. Please try again later."


def find_actor_by_birthdate(birthdate_str: str) -> str:
    try:
        date_obj = datetime.strptime(birthdate_str, "%Y-%m-%d")
        month_day = date_obj.strftime("%m-%d")
        local = ACTORS.get(month_day)
        if local:
            return local
        month, day = month_day.split("-")
        return _search_wikipedia_births(month, day)
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/match", methods=["POST"])
def match():
    data = request.get_json()
    name = (data.get("name") or "").strip() or "Guest"
    birthdate = data.get("birthdate", "")
    actor = find_actor_by_birthdate(birthdate)
    return jsonify({"name": name, "actor": actor})


def cli():
    print("Welcome to the Birthday Actor Matcher!")
    name = input("What is your name? ").strip() or "Guest"
    birthdate = input("Enter your birthdate (YYYY-MM-DD): ")
    actor = find_actor_by_birthdate(birthdate)
    print(f"\nHello {name}!")
    print(f"An American male actor born on your date is: {actor}")


if __name__ == "__main__":
    if "--cli" in sys.argv:
        cli()
    else:
        app.run(debug=True)
