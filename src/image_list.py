import collections
import logging
from data_structs.image import Image
from db_base import DbBase


class ImageList:
    def __init__(self, db: DbBase):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._db = db
        self._image_list = self._db.get_all_images_in_db()
        self._last_shown_images_size = 10
        self._last_shown_images = collections.deque(maxlen=self._last_shown_images_size)
        self._last_shown_image_ix = None
        self._image_index = 0

    def get_next_image(self) -> Image:
        # if we are currently showing historical image (that was already shown, we went back)
        # then show the next in the history list
        if self._last_shown_image_ix is not None:
            if self._last_shown_image_ix > 1:
                self._last_shown_image_ix -= 1
                return self._last_shown_images[-self._last_shown_image_ix]
            else:
                self._last_shown_image_ix = None

        # else: find a new image to show
        if self._image_index < len(self._image_list) - 1:
            self._image_index += 1
        else:
            # when we went through the full list we can update the list from the DB
            self._update_image_list()
            self._image_index = 0

        im = self._image_list[self._image_index - 1]
        self._last_shown_images.append(im)
        return im

    def get_last_shown_image(self):
        if self._last_shown_image_ix is None:
            self._last_shown_image_ix = 1
            return self._last_shown_images[-self._last_shown_image_ix]
        elif self._last_shown_image_ix < self._last_shown_images_size:
            self._last_shown_image_ix += 1
            return self._last_shown_images[-self._last_shown_image_ix]
        else:  # we want back to the last history image
            return self._last_shown_images[0]

    def _update_image_list(self):
        db_images_count = self._db.get_images_count()
        if db_images_count != len(self._image_list):
            self._image_list = self._db.get_all_images_in_db()
