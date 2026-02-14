import sys
from datetime import datetime

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


def find_actor_by_birthdate(birthdate_str: str) -> str:
    try:
        date_obj = datetime.strptime(birthdate_str, "%Y-%m-%d")
        month_day = date_obj.strftime("%m-%d")
        return ACTORS.get(month_day, "No matching actor found.")
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
