class Time:
    CYCLE = ["morning", "day", "evening", "night"]

    def __init__(self):
        self.current_index = 0

    def advance(self):
        self.current_index = (self.current_index + 1) % len(self.CYCLE)

    def get_time(self):
        return self.CYCLE[self.current_index]
