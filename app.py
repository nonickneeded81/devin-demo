import os
from datetime import datetime, timedelta, timezone

import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

ODDS_API_KEY = os.environ.get("ODDS_API_KEY", "")
SPORT_KEY = "soccer_germany_bundesliga"
ODDS_API_BASE = "https://api.the-odds-api.com/v4/sports"

TEAM_LOGOS = {
    "Bayern Munich": "https://media.api-sports.io/football/teams/157.png",
    "FC Bayern Munich": "https://media.api-sports.io/football/teams/157.png",
    "Borussia Dortmund": "https://media.api-sports.io/football/teams/165.png",
    "RB Leipzig": "https://media.api-sports.io/football/teams/173.png",
    "Bayer Leverkusen": "https://media.api-sports.io/football/teams/168.png",
    "Bayer 04 Leverkusen": "https://media.api-sports.io/football/teams/168.png",
    "Eintracht Frankfurt": "https://media.api-sports.io/football/teams/169.png",
    "VfB Stuttgart": "https://media.api-sports.io/football/teams/172.png",
    "SC Freiburg": "https://media.api-sports.io/football/teams/160.png",
    "Sport-Club Freiburg": "https://media.api-sports.io/football/teams/160.png",
    "TSG Hoffenheim": "https://media.api-sports.io/football/teams/167.png",
    "1899 Hoffenheim": "https://media.api-sports.io/football/teams/167.png",
    "VfL Wolfsburg": "https://media.api-sports.io/football/teams/161.png",
    "1. FC Union Berlin": "https://media.api-sports.io/football/teams/182.png",
    "Union Berlin": "https://media.api-sports.io/football/teams/182.png",
    "Borussia Monchengladbach": "https://media.api-sports.io/football/teams/163.png",
    "Borussia Mönchengladbach": "https://media.api-sports.io/football/teams/163.png",
    "Werder Bremen": "https://media.api-sports.io/football/teams/162.png",
    "SV Werder Bremen": "https://media.api-sports.io/football/teams/162.png",
    "1. FSV Mainz 05": "https://media.api-sports.io/football/teams/164.png",
    "Mainz 05": "https://media.api-sports.io/football/teams/164.png",
    "FC Augsburg": "https://media.api-sports.io/football/teams/170.png",
    "1. FC Heidenheim": "https://media.api-sports.io/football/teams/180.png",
    "1. FC Heidenheim 1846": "https://media.api-sports.io/football/teams/180.png",
    "FC St. Pauli": "https://media.api-sports.io/football/teams/186.png",
    "Holstein Kiel": "https://media.api-sports.io/football/teams/192.png",
    "SV Darmstadt 98": "https://media.api-sports.io/football/teams/181.png",
    "1. FC Köln": "https://media.api-sports.io/football/teams/177.png",
    "1. FC Koln": "https://media.api-sports.io/football/teams/177.png",
    "Hertha BSC": "https://media.api-sports.io/football/teams/159.png",
    "FC Schalke 04": "https://media.api-sports.io/football/teams/174.png",
}

DEFAULT_LOGO = "https://media.api-sports.io/football/teams/0.png"


def get_team_logo(team_name):
    if team_name in TEAM_LOGOS:
        return TEAM_LOGOS[team_name]
    for key, url in TEAM_LOGOS.items():
        if key.lower() in team_name.lower() or team_name.lower() in key.lower():
            return url
    return DEFAULT_LOGO


def get_weekend_range():
    now = datetime.now(timezone.utc)
    weekday = now.weekday()
    if weekday < 4:
        days_until_friday = 4 - weekday
    elif weekday == 4:
        days_until_friday = 0
    elif weekday in (5, 6):
        days_until_friday = 0
    else:
        days_until_friday = 4 - weekday + 7

    if weekday in (5, 6):
        friday = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=weekday - 4)
    else:
        friday = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=days_until_friday)

    monday = friday + timedelta(days=3)
    return friday, monday


def fetch_odds():
    if not ODDS_API_KEY:
        return None, "API key not configured. Set the ODDS_API_KEY environment variable."

    url = f"{ODDS_API_BASE}/{SPORT_KEY}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal",
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.HTTPError:
        if resp.status_code == 401:
            return None, "Invalid API key. Check your ODDS_API_KEY."
        if resp.status_code == 422:
            return None, "Bundesliga odds are not currently available (off-season or no upcoming matches)."
        return None, f"API error: {resp.status_code}"
    except Exception as e:
        return None, f"Failed to fetch odds: {e}"


def aggregate_matches(raw_events):
    friday, monday = get_weekend_range()
    matches = []

    for event in raw_events:
        commence = datetime.fromisoformat(event["commence_time"].replace("Z", "+00:00"))
        if not (friday <= commence < monday):
            continue

        home_team = event["home_team"]
        away_team = event["away_team"]

        home_odds_list = []
        draw_odds_list = []
        away_odds_list = []
        bookmaker_names = []

        for bookmaker in event.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market["key"] != "h2h":
                    continue
                outcomes = {o["name"]: o["price"] for o in market["outcomes"]}
                home_price = outcomes.get(home_team)
                away_price = outcomes.get(away_team)
                draw_price = outcomes.get("Draw")
                if home_price and away_price and draw_price:
                    home_odds_list.append(home_price)
                    away_odds_list.append(away_price)
                    draw_odds_list.append(draw_price)
                    bookmaker_names.append(bookmaker["title"])

        if not home_odds_list:
            continue

        matches.append({
            "home_team": home_team,
            "away_team": away_team,
            "home_logo": get_team_logo(home_team),
            "away_logo": get_team_logo(away_team),
            "commence_time": event["commence_time"],
            "avg_home": round(sum(home_odds_list) / len(home_odds_list), 2),
            "avg_draw": round(sum(draw_odds_list) / len(draw_odds_list), 2),
            "avg_away": round(sum(away_odds_list) / len(away_odds_list), 2),
            "num_bookmakers": len(home_odds_list),
            "bookmakers": bookmaker_names,
        })

    matches.sort(key=lambda m: m["commence_time"])
    return matches


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/odds")
def api_odds():
    raw, error = fetch_odds()
    if error:
        return jsonify({"error": error, "matches": []}), 200

    matches = aggregate_matches(raw)
    friday, monday = get_weekend_range()
    return jsonify({
        "matches": matches,
        "weekend": {
            "from": friday.isoformat(),
            "to": monday.isoformat(),
        },
        "total_events": len(raw),
    })


if __name__ == "__main__":
    app.run()
