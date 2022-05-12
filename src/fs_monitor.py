import logging
from typing import Dict

from configuration import Configuration
from db_base import DbBase
from data_structs.image import Image


class FileSystemMonitor:
    def __init__(self, cfg: Configuration, db: DbBase):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._cfg = cfg
        self._db = db
        self._cache: Dict[str, Image] = self._create_cache()

    def run(self):
        # monitor files in paths (cfg)
        # add/ remove from local cache + db
        pass

    def _create_cache(self):
        db_images = self._db.get_all_images_in_db()
        c = dict()
        for i in db_images:
            c[i.image_path] = i
        self._logger.info(f'initialized local cache with {len(c)} images')
        return c