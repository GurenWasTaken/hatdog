import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "settings.json")

DEFAULT_CONFIG = {
    "accounts": [
        {"id": 1, "alias": "Account 1"},
        {"id": 2, "alias": "Account 2"},
        {"id": 3, "alias": "Account 3"}
    ],
    "delays": {
        "after_launch": 3.0,
        "after_switch": 2.0
    },
    "logging_enabled": True
}


def load_config():
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def update_alias(account_id, new_alias):
    config = load_config()
    for acc in config["accounts"]:
        if acc["id"] == account_id:
            acc["alias"] = new_alias
            break
    save_config(config)
    return config
