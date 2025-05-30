from plants.base_plant import BasePlant

class Obscurite(BasePlant):
    def __init__(self):
        super().__init__()
        self.symbol = "O"

    def adapt_to_time(self, time_of_day):
        # Активен только при "night" (ночь)
        self.active = (time_of_day == "night")
