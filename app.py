import re

_DATE_RE = re.compile(r"^\d{4}-(\d{2}-\d{2})$")

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
    "12-18": "Brad Pitt"
}


def find_actor_by_birthdate(birthdate_str: str) -> str:
    """
    Takes a birthdate string (YYYY-MM-DD),
    extracts month and day,
    and returns a matching actor if available.
    """
    match = _DATE_RE.match(birthdate_str)
    if not match:
        return "Invalid date format. Please use YYYY-MM-DD."
    month_day = match.group(1)
    return ACTORS.get(month_day, "No matching actor found.")


def main():
    print("Welcome to the Birthday Actor Matcher!")
    
    name = input("What is your name? ")
    birthdate = input("Enter your birthdate (YYYY-MM-DD): ")
    
    actor = find_actor_by_birthdate(birthdate)
    
    print(f"\nHello {name}!")
    print(f"An American male actor born on your date is: {actor}")


if __name__ == "__main__":
    main()
