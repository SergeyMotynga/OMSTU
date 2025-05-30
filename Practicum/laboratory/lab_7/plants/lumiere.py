from plants.base_plant import BasePlant

class Lumiere(BasePlant):
    def __init__(self):
        super().__init__()
        self.symbol = "L"

    def adapt_to_time(self, time_of_day):
        # Активен только при "day" (день)
        self.active = (time_of_day == "day")
