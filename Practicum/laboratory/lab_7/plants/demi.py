from plants.base_plant import BasePlant

class Demi(BasePlant):
    def __init__(self):
        super().__init__()
        self.symbol = "D"

    def adapt_to_time(self, time_of_day):
        # Активен при "morning" и "evening" (утро и вечер)
        self.active = (time_of_day == "morning" or time_of_day == "evening")
