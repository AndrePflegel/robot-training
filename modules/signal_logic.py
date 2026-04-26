def resolve_action(profile, signals):
    rules = profile.get("signal_rules", {})
    actions = profile.get("actions", {})

    # Priorität: STOP zuerst
    if "color_rot" in signals:
        return actions.get(rules.get("color_rot"), "STOP")

    if "color_gruen" in signals:
        return actions.get(rules.get("color_gruen"), "GO")

    if "line_left" in signals:
        return actions.get(rules.get("line_left"), "TURN_LEFT")

    if "line_center" in signals:
        return actions.get(rules.get("line_center"), "FORWARD")

    if "line_right" in signals:
        return actions.get(rules.get("line_right"), "TURN_RIGHT")

    for s in signals:
        if s.startswith("digit_"):
            return actions.get(rules.get(s), "WAIT")

    return actions.get("WAIT", "WAIT")
