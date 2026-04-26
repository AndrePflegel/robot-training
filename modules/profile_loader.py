import json
import os


DEFAULT_PROFILE_PATH = "config/profiles.json"


def load_profiles(path=DEFAULT_PROFILE_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Profil-Datei nicht gefunden: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_active_profile(data):
    active_name = data.get("active_profile")

    if active_name is None:
        raise ValueError("Kein active_profile angegeben.")

    profiles = data.get("profiles", {})

    if active_name not in profiles:
        raise ValueError(f"Aktives Profil nicht gefunden: {active_name}")

    return profiles[active_name]


def get_enabled_detectors(profile):
    detectors = profile.get("detectors", {})

    return [
        name
        for name, enabled in detectors.items()
        if enabled is True
    ]


def get_model_config(profile, model_type):
    models = profile.get("models", {})

    if model_type not in models:
        raise ValueError(f"Modelltyp nicht gefunden: {model_type}")

    return models[model_type]
