from strategies.rectangular_strategy import RectangularStrategy


STRATEGIES = {
    "rectangular": RectangularStrategy
}

class PlacementHandler:
    def __init__(self, roof_type) -> None:
        self.strategy = STRATEGIES[roof_type]()

    def place_solar_panels(self, roof, solar_panel):
        return self.strategy.find_optimal_arrangement(roof, solar_panel)
