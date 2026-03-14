import csv
import os

# get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# build full path to users.csv
USER_FILE = os.path.join(BASE_DIR, "users.csv")


def load_users():
    """Load user records from the CSV file."""

    users = []

    with open(USER_FILE, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not row:
                continue

            cleaned_row = {}

            for k, v in row.items():
                # skip invalid keys
                if k is None:
                    continue

                key = k.strip()
                value = v.strip() if isinstance(v, str) else ""

                cleaned_row[key] = value

            # skip blank rows
            if not cleaned_row.get("username"):
                continue

            # convert permission strings into boolean values
            cleaned_row["can_play"] = cleaned_row.get("can_play", "").lower() == "true"
            cleaned_row["can_dashboard"] = cleaned_row.get("can_dashboard", "").lower() == "true"
            cleaned_row["can_balance"] = cleaned_row.get("can_balance", "").lower() == "true"

            users.append(cleaned_row)

    return users


def check_login(username, password):
    """Return the matching user if credentials are correct."""

    users = load_users()

    for user in users:
        if user["username"] == username and user["password"] == password:
            return user

    return None


def get_permissions(user):
    """Return a dictionary of permissions for the user."""

    return {
        "play": user["can_play"],
        "dashboard": user["can_dashboard"],
        "balance": user["can_balance"],
    }