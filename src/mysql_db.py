import logging
from typing import List
import sqlite3
from datetime import datetime

from db_base import DbBase
from data_structs.image import Image


class MySqlDb(DbBase):

    IMAGES_TABLE_NAME = 'images'
    CREATE_IMAGES_Q = \
    f"""
    CREATE TABLE {IMAGES_TABLE_NAME} (
        image_path TEXT PRIMARY KEY,
        view_count INTEGER,
        last_view_ts TIMESTAMP,
        do_not_show_image INTEGER,
        comment TEXT
    );
    """

    ADD_IMAGE_Q = \
    f"""
    INSERT INTO {IMAGES_TABLE_NAME} (image_path, view_count, last_view_ts, do_not_show_image, comment)
    VALUES (?,?,?,?,?)
    """

    REMOVE_IMAGE_Q = \
    f"""
    DELETE FROM {IMAGES_TABLE_NAME}
    WHERE image_path = ?
    """

    GET_IMAGES_Q = \
    f"""
    SELECT * FROM {IMAGES_TABLE_NAME}
    """

    GET_IMAGES_COUNT_Q = \
    f"""
    SELECT count(*) FROM {IMAGES_TABLE_NAME}
    """

    GET_IMAGE_Q = \
    f"""
    SELECT * FROM {IMAGES_TABLE_NAME}
    WHERE image_path = ?
    """

    UPDATE_IMAGE_VIEWS_Q = \
    f"""
    UPDATE {IMAGES_TABLE_NAME}
    SET view_count = ?
    WHERE image_path = ?
    """

    UPDATE_IMAGE_LAST_VIEW_TIME_Q = \
    f"""
    UPDATE {IMAGES_TABLE_NAME}
    SET last_view_ts = ?
    WHERE image_path = ?
    """

    def __init__(self, db_file: str):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._con = sqlite3.connect(db_file, check_same_thread=False)
        self._con.row_factory = sqlite3.Row
        self._initialize_db()

    def add_image_to_db(self, im: Image):
        self._logger.debug(f'adding {im} into DB')
        self._con.execute(self.ADD_IMAGE_Q, (im.image_path,
                                             im.view_count,
                                             im.last_view_ts,
                                             im.do_not_show_image,
                                             im.comment))
        self._con.commit()

    def remove_image_from_db(self, im: Image):
        self._logger.debug(f'removing {im} from DB')
        self._con.execute(self.REMOVE_IMAGE_Q, (im.image_path,))
        self._con.commit()

    def get_all_images_in_db(self) -> List[Image]:
        c = self._con.execute(self.GET_IMAGES_Q)
        images = []
        for row in c:
            images.append(Image(image_path=row['image_path'],
                                view_count=row['view_count'],
                                last_view_ts=row['last_view_ts'],
                                do_not_show_image=row['do_not_show_image'],
                                comment=row['comment'])
            )

        self._logger.debug(f'get_all_images_in_db found {len(images)} images')
        return images

    def get_images_count(self) -> int:
        c = self._con.execute(self.GET_IMAGES_COUNT_Q)
        return c.fetchone()[0]

    def update_image_view_count(self, image: Image) -> int:
        c = self._con.execute(self.GET_IMAGE_Q, (image.image_path,))
        im = c.fetchone()
        current_views = im['view_count']
        self._con.execute(self.UPDATE_IMAGE_VIEWS_Q, (current_views + 1, image.image_path))
        self._con.commit()
        return current_views + 1

    def update_image_last_view_timestamp(self, image: Image, timestamp: datetime):
        self._con.execute(self.UPDATE_IMAGE_LAST_VIEW_TIME_Q, (timestamp, image.image_path))
        self._con.commit()

    def _initialize_db(self):
        c = self._con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (self.IMAGES_TABLE_NAME,))
        if len(c.fetchall()) == 0:  # no table for images yet
            self._logger.info(f'{self.IMAGES_TABLE_NAME} table not created yet, creating')
            self._con.execute(self.CREATE_IMAGES_Q)
            self._con.commit()
