import json
import os

FILE_NAME = "applications.json"

def load_data():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)
