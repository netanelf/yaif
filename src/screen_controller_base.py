from abc import ABC, abstractmethod


class ScreenControllerBase(ABC):
    @abstractmethod
    def turn_off_screen(self):
        pass

    @abstractmethod
    def turn_on_screen(self):
        pass