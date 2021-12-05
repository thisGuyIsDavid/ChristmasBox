import time

from rpi_ws281x import PixelStrip, Color


class ChristmasLights:

    def __init__(self):
        self.strip = PixelStrip(55, 18, 800000, 10, False, 255, 0)
        self.strip.begin()

    def set_tree_light(self, position, color):
        converted_position = position if position < 16 else (20 + (position - 15))
        print(position, converted_position)
        self.strip.setPixelColor(converted_position, color)

    def set_star_light(self, position, color):
        position = 40 + position
        self.strip.setPixelColor(position, color)

    def light_tree(self, color, wait_ms=50):
        for i in range(32):
            self.set_tree_light(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def light_trunk(self, color, wait_ms=50):
        for i in range(16, 20):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
        for i in range(36, 40):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

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

    def twinkle_star(self, tick, wait_ms=250):
        for i in range(40, 47):
            color = self.wheel(35 + ((i + tick) % 30))
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def twinkle_tree(self, tick):
        for i in range(32):
            color = self.wheel(((i + tick) % 30))
            self.light_tree(i, color)
        self.strip.show()

    def run(self):
        self.light_tree(Color(0, 255, 0))

if __name__ == '__main__':
    ChristmasLights().run()