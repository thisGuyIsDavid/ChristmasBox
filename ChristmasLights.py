import time

from rpi_ws281x import PixelStrip, Color


class ChristmasLights:

    TREE_COLORS = [Color(0, 255, 0), Color(0, 128, 128), Color(255, 0, 0), Color(255, 255, 255)]
    STAR_COLORS = [Color(128, 128, 0), Color(255, 255, 255), Color(0, 255, 0), Color(255, 0, 0)]

    def __init__(self):
        self.strip = PixelStrip(55, 18, 800000, 10, False, 255, 0)
        self.strip.begin()
        self.scheme = 0

        self.tree_colors = []
        self.star_colors = []
        self.trunk_colors = []

    #   TREE LIGHTS
    def set_tree_colors(self, color_array):
        self.tree_colors = color_array

    def set_tree_light(self, position, color):
        converted_position = position if position < 16 else (20 + (position - 16))
        self.strip.setPixelColor(converted_position, color)

    def light_tree(self, wait_ms=50):
        for i in range(32):
            self.set_tree_light(i, self.TREE_COLORS[self.scheme])
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def twinkle_tree(self, tick):
        for i in range(32):
            color = self.tree_colors[(i+tick) % len(self.tree_colors)]
            self.set_tree_light(i, color)
        self.strip.show()

    #   STAR LIGHTS
    def set_star_colors(self, color_array):
        self.star_colors = color_array

    def set_star_light(self, position, color):
        position = 40 + position
        self.strip.setPixelColor(position, color)

    def light_star(self, wait_ms=50):
        for i in range(0, 7):
            self.set_star_light(i, self.STAR_COLORS[self.scheme])
            self.strip.show()
            time.sleep(wait_ms / 1000)

    def twinkle_star(self, tick):
        for i in range(0, 7):
            color = self.star_colors[(i+tick) % len(self.star_colors)]
            self.set_star_light(i, color)
        self.strip.show()

    #   Trunk
    def set_trunk_colors(self, color_array):
        self.trunk_colors = color_array

    def set_trunk_light(self, position, color):
        if position < 4:
            converted_position = 16 + position
        else:
            converted_position = 36 + (position - 4)
        self.strip.setPixelColor(converted_position, color)

    def light_trunk(self, wait_ms=50):
        for i in range(8):
            self.set_trunk_light(i, self.trunk_colors[0])
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def clear_all_lights(self, wait_ms=50):
        for i in range(53):
            self.strip.setPixelColor(i, Color(0, 0, 0))
            self.strip.show()
            time.sleep(wait_ms / 1000)

    #   Presents
    def light_traditional(self):
        self.set_tree_colors(
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
        self.set_star_colors(
            [
                Color(90, 165, 0),
                Color(93, 162, 0),
                Color(96, 159, 0),
                Color(99, 156, 0),
                Color(102, 153, 0),
                Color(105, 150, 0),
                Color(108, 147, 0),
                Color(111, 144, 0),
                Color(114, 141, 0),
                Color(117, 138, 0)
            ]
        )

    def run(self):
        try:
            tick_count = 0
            while True:
                self.light_tree()
                self.light_star()
                time.sleep(15)
                tick_count += 1
                self.scheme = tick_count % len(self.TREE_COLORS)
        except KeyboardInterrupt:
            pass
        finally:
            self.clear_all_lights()

if __name__ == '__main__':
    christmas_lights = ChristmasLights()
    christmas_lights.run()