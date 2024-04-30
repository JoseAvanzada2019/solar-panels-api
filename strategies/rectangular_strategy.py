import copy

HEIGHT = "height"
WIDTH = "width"

class RectangularStrategy:
    def __init__(self) -> None:
        self.memory = {}

    def solar_panel_fits_in_roof(self, roof, solar_panel):
        fits_normal = solar_panel[WIDTH] <= roof[WIDTH] and solar_panel[HEIGHT] <= roof[HEIGHT]
        fits_flipped = solar_panel[HEIGHT] <= roof[WIDTH] and solar_panel[WIDTH] <= roof[HEIGHT]
        return fits_normal or fits_flipped
    
    def unidimentional_fit(self, roof, solar_panel):
        return solar_panel[WIDTH] <= roof[WIDTH] and solar_panel[HEIGHT] <= roof[HEIGHT]
        
    # NOTE: entrypoint for strategy
    def find_optimal_arrangement(self, roof, solar_panel):
        if (roof[WIDTH], roof[HEIGHT]) in self.memory:
            return self.memory[(roof[WIDTH], roof[HEIGHT])]
        if not self.solar_panel_fits_in_roof(roof, solar_panel):
            self.memory[(roof[WIDTH], roof[HEIGHT])] = []    
            return []

        else:
            best_arrangement = []
            placements = []
            if self.unidimentional_fit(roof, { WIDTH: solar_panel[WIDTH], HEIGHT: solar_panel[HEIGHT] }):
                placements.append((solar_panel[WIDTH], solar_panel[HEIGHT]))
            if self.unidimentional_fit(roof, { WIDTH: solar_panel[HEIGHT], HEIGHT: solar_panel[WIDTH] }):
                placements.append((solar_panel[HEIGHT], solar_panel[WIDTH]))
            for x, y in placements:
                # rectangulo lado largo
                roof_1 = { WIDTH: roof[WIDTH] - x, HEIGHT: roof[HEIGHT] }
                arrangement_1 = self.find_optimal_arrangement(roof_1, solar_panel)
                # rectangulo base corto
                # NOTE: aca no deberia haber un max, si no cabe en este sentido no deberia ser opcion
                roof_2 = { WIDTH: x, HEIGHT: roof[HEIGHT] - y }
                arrangement_2 = self.find_optimal_arrangement(roof_2, solar_panel)
                # rectangulo lado corto
                roof_3 = { WIDTH: roof[WIDTH] - x, HEIGHT: y }
                arrangement_3 = self.find_optimal_arrangement(roof_3, solar_panel)
                # rectangulo base largo
                roof_4 = { WIDTH: roof[WIDTH], HEIGHT: roof[HEIGHT] - y}
                arrangement_4 = self.find_optimal_arrangement(roof_4, solar_panel)

                if len(arrangement_1) + len(arrangement_2) > len(arrangement_3) + len(arrangement_4):
                    current_arrangement = self.translate_rectangles(arrangement_1, (x, 0)) + self.translate_rectangles(arrangement_2, (0, y))
                else:
                    current_arrangement = self.translate_rectangles(arrangement_3, (x, 0)) + self.translate_rectangles(arrangement_4, (0, y))
                current_arrangement += [{"x": 0, "y": 0, "width": x, "height": y}]
                if len(current_arrangement) > len(best_arrangement):
                    best_arrangement = current_arrangement
            # no entiendo pq el +1 y el cero, no deberian darte ambas 0 en ese caso y seria redundante?
            # si ya revisamos arriba que cabia, entonces asumimos que lo vamos a poner no+ no?
            self.memory[(roof[WIDTH], roof[HEIGHT])] = best_arrangement
            
            return best_arrangement
        
    def translate_rectangles(self, rectangles, translation):
        """
        Translates coordinates based on a given rectangle's position.

        Parameters:
        - rectangle: A tuple (rect_x, rect_y) representing the position of the rectangle.
        - coordinates: A list of dictionaries, each containing keys "x" and "y" representing coordinates.

        Returns:
        A list of dictionaries with translated coordinates.
        """
        rect_x, rect_y = translation
        translated_rectangles = []
        for rect in rectangles:
            x = rect["x"] + rect_x
            y = rect["y"] + rect_y
            translated_rectangles.append({"x": x, "y": y, "width": rect["width"], "height": rect["height"]})
        return translated_rectangles
