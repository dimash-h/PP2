import json
import os

# --- PATH CONFIGURATION ---
# Determine the directory of the current script to ensure JSON files are saved in the same folder
BASE_DIR = os.path.dirname(__file__)
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")
SETTINGS_FILE    = os.path.join(BASE_DIR, "settings.json")

# --- 1. SETTINGS MANAGEMENT ---

# Default values used if the settings file is missing or corrupted
DEFAULT_SETTINGS = {
    "car_color": [0, 100, 255],
    "sound": False,
    "difficulty": "normal"
}

def load_settings():
    """Reads settings from the JSON file or returns defaults if file doesn't exist."""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        return dict(DEFAULT_SETTINGS)
    except (json.JSONDecodeError, IOError):
        # Fallback to defaults if file is unreadable or empty
        return dict(DEFAULT_SETTINGS)

def save_settings(settings):
    """Saves the current settings dictionary to the settings.json file."""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except IOError as e:
        print(f"Error saving settings: {e}")


# --- 2. LEADERBOARD MANAGEMENT ---

def load_leaderboard():
    """Loads the list of high scores from the JSON file."""
    try:
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f)
        return []
    except (json.JSONDecodeError, IOError):
        # Return an empty list if file is missing or corrupted
        return []

def save_leaderboard(records):
    """Writes the updated leaderboard list to the leaderboard.json file."""
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(records, f, indent=4)
    except IOError as e:
        print(f"Error saving leaderboard: {e}")

def add_record(username, score, distance, coins):
    """
    Adds a new performance record, sorts the leaderboard by score (descending),
    and keeps only the top 10 players.
    """
    records = load_leaderboard()
    
    # Create the new record entry
    new_entry = {
        "name": username,
        "score": score,
        "distance": distance,
        "coins": coins
    }
    
    records.append(new_entry)
    
    # Sort the list by the 'score' key in descending order
    # [:10] slices the list to keep only the top 10 results
    records = sorted(records, key=lambda x: x["score"], reverse=True)[:10]
    
    # Save the updated top 10 list back to disk
    save_leaderboard(records)