import time

from rpi_ws281x import PixelStrip, Color


class ChristmasLights:

    def __init__(self):
        self.strip = PixelStrip(55, 18, 800000, 10, False, 255, 0)
        self.strip.begin()

        self.tree_colors = []
        self.star_colors = []

    #   TREE LIGHTS
    def set_tree_colors(self, color_array):
        self.tree_colors = color_array

    def set_tree_light(self, position, color):
        converted_position = position if position < 16 else (20 + (position - 16))
        self.strip.setPixelColor(converted_position, color)

    def light_tree(self, wait_ms=50):
        for i in range(32):
            self.set_tree_light(i, self.tree_colors[0])
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def twinkle_tree(self, tick):
        for i in range(32):
            color = self.tree_colors[(i+tick) % len(self.tree_colors)]
            self.set_tree_light(i, color)
        self.strip.show()




    @staticmethod
    def wheel(pos):
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    #   Light setters.


    def set_star_light(self, position, color):
        position = 40 + position
        self.strip.setPixelColor(position, color)

    def set_trunk_light(self, position, color):
        if position < 4:
            converted_position = 16 + position
        else:
            converted_position = 36 + (position - 4)
        self.strip.setPixelColor(converted_position, color)

    #   Solid lighting.


    def light_star(self, color, wait_ms=50):
        for i in range(0, 7):
            self.set_star_light(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000)

    def light_trunk(self, color, wait_ms=50):
        for i in range(8):
            self.set_trunk_light(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    #   Twinkle lighting.
    def twinkle_star(self, tick):
        for i in range(0, 7):
            color = self.wheel(35 + ((i + tick) % 15))
            self.set_star_light(i, color)
        self.strip.show()

    def clear_all_lights(self, wait_ms=50):
        for i in range(53):
            self.strip.setPixelColor(i, Color(0, 0, 0))
            self.strip.show()
            time.sleep(wait_ms / 1000)

    def run(self):

        try:
            tick_count = 0
            while True:
                self.twinkle_tree(tick_count)
                time.sleep(150/1000)
                tick_count += 1
        except KeyboardInterrupt:
            pass
        finally:
            self.clear_all_lights()

if __name__ == '__main__':
    christmas_lights = ChristmasLights()
    christmas_lights.set_tree_colors(
        [
            Color(3, 252, 0),
            Color(6, 249, 0),
            Color(9, 246, 0),
            Color(12, 243, 0),
            Color(15, 240, 0),
            Color(18, 237, 0),
            Color(21, 234, 0),
            Color(24, 231, 0),
            Color(27, 228, 0),
            Color(30, 225, 0),
            Color(33, 222, 0),
            Color(36, 219, 0),
            Color(39, 216, 0)
        ]

    )
    christmas_lights.light_tree()
    christmas_lights.run()