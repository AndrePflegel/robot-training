# modules/mission_control.py

class MissionController:

    def __init__(self):
        self.state = "IDLE"
        self.mode = None
        self.sequence = []
        self.current_index = 0

    def reset(self):
        self.state = "IDLE"
        self.mode = None
        self.sequence = []
        self.current_index = 0

    def set_mode(self, mode):
        self.mode = mode

        if mode == 1:
            self.sequence = ["gruen"]

        elif mode == 2:
            self.sequence = ["rot", "blau"]

        elif mode == 3:
            self.sequence = ["rot", "gruen", "blau"]

        self.current_index = 0
        self.state = "RUNNING"

    def get_current_target(self):
        if self.current_index >= len(self.sequence):
            return None

        return self.sequence[self.current_index]

    def target_reached(self):
        self.current_index += 1

        if self.current_index >= len(self.sequence):
            self.state = "FINISHED"

    def is_running(self):
        return self.state == "RUNNING"

    def is_finished(self):
        return self.state == "FINISHED"
