import logging
import time

import RPi.GPIO as GPIO

from src.screen_controller_base import ScreenControllerBase
from src.configuration import Configuration, get_default_configuration


class ScreenController10i(ScreenControllerBase):
    SCREEN_ON = 1
    SCREEN_OFF = 0

    def __init__(self, configuration: Configuration):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._cfg = configuration

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._cfg.screen_enable_pin_number, GPIO.OUT)

    def turn_on_screen(self):
        self._logger.debug('Turning screen ON')
        GPIO.output(self._cfg.screen_enable_pin_number, self.SCREEN_ON)

    def turn_off_screen(self):
        self._logger.debug('Turning screen OFF')
        GPIO.output(self._cfg.screen_enable_pin_number, self.SCREEN_OFF)


if __name__ == '__main__':
    s = ScreenController10i(get_default_configuration())
    for i in range(5):
        s.turn_on_screen()
        time.sleep(10)
        s.turn_off_screen()
        time.sleep(10)
