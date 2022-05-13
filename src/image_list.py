import logging
from data_structs.image import Image
from db_base import DbBase


class ImageList:
    def __init__(self, db: DbBase):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._db = db

    def get_next_image(self) -> Image:
        #self._db.update_image_last_view_timestamp() ? are wesure it was shown? maybe the display should update?
        pass