# ai-escape-app/data/game_settings.py

GAME_SETTINGS = {
    "sound": {
        "title": "Sound Effects Volume",
        "type": "slider",
        "default": 80,
        "min": 0,
        "max": 100,
        "step": 1
    },
    "music": {
        "title": "Music Volume",
        "type": "slider",
        "default": 60,
        "min": 0,
        "max": 100,
        "step": 1
    },
    "language": {
        "title": "Language",
        "type": "select",
        "default": "en",
        "options": [
            {"value": "en", "label": "English"},
            {"value": "es", "label": "Español (placeholder)"},
            {"value": "fr", "label": "Français (placeholder)"}
        ]
    }
}
