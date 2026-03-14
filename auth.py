import csv
import os

# get the absolute path of this file's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# build path to users.csv so it works regardless of working directory
USER_FILE = os.path.join(BASE_DIR, "users.csv")


def load_users():
    """Load users from CSV and convert permission fields to booleans."""

    users = []

    with open(USER_FILE, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:

            # remove leading/trailing whitespace from CSV values
            cleaned_row = {k.strip(): v.strip() for k, v in row.items()}

            # convert string permission flags to booleans
            cleaned_row["can_play"] = cleaned_row["can_play"].lower() == "true"
            cleaned_row["can_dashboard"] = cleaned_row["can_dashboard"].lower() == "true"
            cleaned_row["can_balance"] = cleaned_row["can_balance"].lower() == "true"

            users.append(cleaned_row)

    return users


def check_login(username, password):
    """Return user dict if credentials match, otherwise None."""

    users = load_users()

    for user in users:
        if user["username"] == username and user["password"] == password:
            return user

    return None


def get_permissions(user):
    """Return permission dictionary for a logged-in user."""

    return {
        "play": user["can_play"],
        "dashboard": user["can_dashboard"],
        "balance": user["can_balance"],
    }