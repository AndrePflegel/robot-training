last_action = None


def execute_action(action):
    global last_action

    left_speed = 0
    right_speed = 0

    if action == "DRIVE_FORWARD_SLOW":
        left_speed = 0.4
        right_speed = 0.4
    elif action == "DRIVE_FORWARD_VERY_SLOW":
        left_speed = 0.2
        right_speed = 0.2
    elif action == "TURN_LEFT":
        left_speed = -0.5
        right_speed = 0.5
    elif action == "TURN_RIGHT":
        left_speed = 0.5
        right_speed = -0.5
    elif action == "CURVE_LEFT":
        left_speed = 0.3
        right_speed = 0.6
    elif action == "CURVE_RIGHT":
        left_speed = 0.6
        right_speed = 0.3
    elif action == "CURVE_LEFT_AWAY_FROM_BOUNDARY":
        left_speed = 0.2
        right_speed = 0.7
    elif action == "CURVE_RIGHT_AWAY_FROM_BOUNDARY":
        left_speed = 0.7
        right_speed = 0.2
    elif action == "TURN_AROUND":
        left_speed = -0.6
        right_speed = 0.6
    elif action == "ESCAPE_CORNER":
        left_speed = -0.4
        right_speed = -0.4
    elif action == "SEARCH_TARGET_SLOW_TURN":
        left_speed = -0.2
        right_speed = 0.3

    if action != last_action:
        print(f"[MOTOR] action={action} | L={left_speed:.2f} R={right_speed:.2f}")
        last_action = action

    return left_speed, right_speed
