from abc import ABC, abstractmethod
from data_structs.image import Image


class DbBase(ABC):
    @abstractmethod
    def add_image_to_db(self, im: Image):
        pass
