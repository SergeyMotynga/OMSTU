class TimeManager:
    def __init__(self):
        self.tick = 0
        self.times_of_day = ['morning', 'day', 'evening', 'night']
        self.time_of_day = self.times_of_day[0]

    def update(self):
        self.tick += 1
        self.time_of_day = self.times_of_day[self.tick % len(self.times_of_day)]