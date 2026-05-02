import json
import os

DB_CONFIG = {
    "host": "localhost",
    "database": "phonebook",
    "user": "postgres",
    "password": "12345678"
}

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": [0, 255, 0],
    "grid": True,
    "sound": True
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)
