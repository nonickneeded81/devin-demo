from datetime import datetime

# A very small dataset of American male actors and their birthdays (month-day)
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
    try:
        date_obj = datetime.strptime(birthdate_str, "%Y-%m-%d")
        month_day = date_obj.strftime("%m-%d")
        return ACTORS.get(month_day, "No matching actor found.")
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."


def main():
    print("Welcome to the Birthday Actor Matcher!")
    
    name = input("What is your name? ")
    birthdate = input("Enter your birthdate (YYYY-MM-DD): ")
    
    actor = find_actor_by_birthdate(birthdate)
    
    print(f"\nHello {name}!")
    print(f"An American male actor born on your date is: {actor}")


if __name__ == "__main__":
    main()
