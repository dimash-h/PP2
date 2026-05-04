import json
import os

#Работа с файлами-рекорды и настройки

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"sound": True, "car_color": "Red", "difficulty": "Normal"} #по умолчанию
    with open(SETTINGS_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {"sound": True, "car_color": "Red", "difficulty": "Normal"}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f) #записали как json

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_leaderboard(leaderboard):
    leaderboard.sort(key=lambda x: x.get("score", 0), reverse=True)
    leaderboard = leaderboard[:10] #топ 10
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f)

def add_score(name, score, distance):
    board = load_leaderboard()
    board.append({"name": name, "score": score, "distance": distance})
    save_leaderboard(board)
