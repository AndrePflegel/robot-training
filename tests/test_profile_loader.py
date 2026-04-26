import json
import pytest

from modules.profile_loader import (
    get_active_profile,
    get_enabled_detectors,
    get_model_config,
    load_profiles,
)


def test_load_profiles(tmp_path):
    data = {
        "active_profile": "default",
        "profiles": {
            "default": {
                "detectors": {}
            }
        }
    }

    path = tmp_path / "profiles.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    result = load_profiles(str(path))

    assert result["active_profile"] == "default"


def test_get_active_profile():
    data = {
        "active_profile": "default",
        "profiles": {
            "default": {
                "detectors": {
                    "colors": True
                }
            }
        }
    }

    profile = get_active_profile(data)

    assert profile["detectors"]["colors"] is True


def test_missing_active_profile_raises_error():
    data = {
        "profiles": {}
    }

    with pytest.raises(ValueError):
        get_active_profile(data)


def test_get_enabled_detectors():
    profile = {
        "detectors": {
            "colors": True,
            "line": False,
            "digits": True
        }
    }

    result = get_enabled_detectors(profile)

    assert result == ["colors", "digits"]


def test_get_model_config():
    profile = {
        "models": {
            "digits": {
                "mode": "dual",
                "available": {
                    "mnist": "models/digit_model.keras"
                }
            }
        }
    }

    result = get_model_config(profile, "digits")

    assert result["mode"] == "dual"
