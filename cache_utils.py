import json
import os

CACHE_FILE = "cache.json"


def load_cache():
    if not os.path.isfile(CACHE_FILE):
        return {
            "monsters_folder": "",
            "output_folder": "",
            "list_file": ""
        }

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "monsters_folder": "",
            "output_folder": "",
            "list_file": ""
        }


def save_cache(monsters_folder, output_folder, list_file):
    data = {
        "monsters_folder": monsters_folder,
        "output_folder": output_folder,
        "list_file": list_file
    }

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
