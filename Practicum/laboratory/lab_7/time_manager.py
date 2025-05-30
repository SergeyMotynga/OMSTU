class TimeManager:
    def __init__(self):
        self.tick = 0
        self.day_length = 40  # Ticks per day
        self.time_of_day = "morning"

    def update(self):
        self.tick = (self.tick + 1) % self.day_length
        phase = self.tick / self.day_length
        if phase < 0.25:
            self.time_of_day = "morning"
        elif phase < 0.5:
            self.time_of_day = "day"
        elif phase < 0.75:
            self.time_of_day = "evening"
        else:
            self.time_of_day = "night"

    def get_light_level(self):
        if self.time_of_day == "day":
            return 1.0  # Full sunlight
        elif self.time_of_day == "night":
            return 0.0  # Moonlight
        else:
            return 0.5  # Low light (morning/evening)