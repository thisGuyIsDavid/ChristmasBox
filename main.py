from DFPlayer import run_dfplayer
import multiprocessing
import logging
from ChristmasLights import ChristmasLights


def run_christmas_box():
    christmas_lights = ChristmasLights()
    christmas_lights.light_traditional()
    christmas_lights.light_tree()
    christmas_lights.light_star()

    button_queue = multiprocessing.Queue()

    dfplayer_process = multiprocessing.Process(target=run_dfplayer, args=(button_queue, ))
