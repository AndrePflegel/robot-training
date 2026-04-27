# modules/motor_control.py

def execute_action(action):
    """
    Wandelt abstrakte Actions in Motorbefehle um.
    Aktuell nur Debug-Ausgabe.
    Später echte Hardware-Ansteuerung.
    """

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

    else:
        left_speed = 0
        right_speed = 0

    # DEBUG (wichtig zum Testen!)
    print(f"[MOTOR] action={action} | L={left_speed:.2f} R={right_speed:.2f}")

    # TODO:
    # hier später echte Motorsteuerung einbauen
    # set_motor_speeds(left_speed, right_speed)
