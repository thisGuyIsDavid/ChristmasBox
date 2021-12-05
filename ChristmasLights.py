#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import PixelStrip, Color
import argparse

class ChristmasLights:
    #   Tree: 0-31
    #   Trunk: 32-39
    #   Star: 40-46


    def __init__(self):
        self.strip = PixelStrip(55, 18, 800000, 10, False, 255, 0)
        self.strip.begin()

    def light_tree(self, color, wait_ms=50):
        for i in range(0, 16):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

        for i in range(20, 36):
            self.strip.setPixelColor(i, color)
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

    def light_star(self, color, wait_ms=50):
        for i in range(40, 47):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def run(self):
        self.light_tree(Color(0, 255, 0))
        #   self.light_trunk(Color(0, 255, 0))
        self.light_star(Color(255, 255, 0))


if __name__ == '__main__':
    ChristmasLights().run()