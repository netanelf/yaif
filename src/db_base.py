from typing import List
from abc import ABC, abstractmethod
from datetime import datetime

from data_structs.image import Image


class DbBase(ABC):
    @abstractmethod
    def add_image_to_db(self, im: Image):
        pass

    @abstractmethod
    def get_all_images_in_db(self) -> List[Image]:
        pass

    @abstractmethod
    def update_image_view_count(self, image: Image) -> int:
        """
        increment view count by one
        :return new image view count
        """
        pass

    @abstractmethod
    def update_image_last_view_timestamp(self, image: Image, timestamp: datetime):
        pass