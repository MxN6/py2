import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(ROOT, "settings.json")
LEADERBOARD_FILE = os.path.join(ROOT, "leaderboard.json")

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "medium"
}

DEFAULT_LEADERBOARD = []


def _ensure_file(path, default_value):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(default_value, handle, indent=2)


def load_json(path, default_value):
    _ensure_file(path, default_value)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError):
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(default_value, handle, indent=2)
        return default_value.copy() if isinstance(default_value, dict) else default_value


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def load_settings():
    return load_json(SETTINGS_FILE, DEFAULT_SETTINGS)


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


def load_leaderboard():
    return load_json(LEADERBOARD_FILE, DEFAULT_LEADERBOARD)


def add_leaderboard_entry(entry):
    leaderboard = load_leaderboard()
    leaderboard.append(entry)
    leaderboard.sort(key=lambda item: (item.get("score", 0), item.get("distance", 0)), reverse=True)
    leaderboard = leaderboard[:10]
    save_leaderboard(leaderboard)
    return leaderboard


def save_leaderboard(leaderboard):
    save_json(LEADERBOARD_FILE, leaderboard)
