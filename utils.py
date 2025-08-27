import json
import re

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))

def validate_phone(phone):
    pattern = r"^\d{7,15}$"
    return bool(re.match(pattern, phone.replace(" ", "")))

def save_candidate_data(data, filename="data/candidates.json"):
    try:
        with open(filename, "r") as f:
            all_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_data = []
    all_data.append(data)
    with open(filename, "w") as f:
        json.dump(all_data, f, indent=2)
