from modules.profile_loader import (
    get_active_profile,
    get_enabled_detectors,
    load_profiles,
)


def run_profile_viewer():
    data = load_profiles()
    profile = get_active_profile(data)

    print()
    print("Aktives Profil")
    print("==============")
    print(data["active_profile"])

    print()
    print("Aktive Erkennungen")
    print("==================")

    for detector in get_enabled_detectors(profile):
        print(f"- {detector}")

    print()
    print("Farben")
    print("======")

    for color in profile.get("colors", []):
        print(
            f"- {color['name']}: "
            f"lower={color['lower']} "
            f"upper={color['upper']} "
            f"action={color['action']}"
        )

    print()
    print("Modelle")
    print("=======")

    for model_type, config in profile.get("models", {}).items():
        print(f"- {model_type}: mode={config.get('mode')}")

        for name, path in config.get("available", {}).items():
            print(f"  - {name}: {path}")

    print()
