from abc import ABC, abstractmethod


class ScreenControllerBase(ABC):
    @abstractmethod
    def shutdown_screen(self):
        pass

    @abstractmethod
    def turn_on_screen(self):
        pass