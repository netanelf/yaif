import logging
import time
from typing import Dict
from pathlib import Path
from threading import Thread

from configuration import Configuration
from db_base import DbBase
from data_structs.image import Image


class FileSystemMonitor:
    def __init__(self, cfg: Configuration, db: DbBase):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._cfg = cfg
        self._db = db
        self._cache: Dict[str, Image] = self._create_cache()
        self._run_periodic_monitor = True
        self._periodic_th = Thread(target=self.run)
        self._periodic_th.setDaemon(True)
        self._periodic_th.start()

    def stop_periodic_monitor(self):
        self._run_periodic_monitor = False

    def run(self):
        self._logger.info('starting periodic monitor thread')
        last_sync_time = 0
        while self._run_periodic_monitor:
            if time.time() - last_sync_time > self._cfg.periodic_monitor_freq_sec:
                self._logger.debug('syncing files')
                # add new files
                for d in self._cfg.image_dirs:
                    for path in Path(d).rglob('*.*'):
                        self._logger.debug(f'found file: {path}')
                        if (path.is_file() and path.suffix[1:] in self._cfg.supported_image_extensions):
                            if path.__str__() in self._cache:
                                continue  # file already in DB and cache
                            else:
                                self._add_image(path)

                # remove deleted files
                for image_dir in list(self._cache.keys()):
                    if not Path(image_dir).exists():
                        self._logger.debug(f'file: {image_dir} seems to be deleted from FS, removing from DB')
                        self._remove_image(self._cache[image_dir])
                last_sync_time = time.time()
            time.sleep(0.5)

    def _create_cache(self):
        db_images = self._db.get_all_images_in_db()
        c = dict()
        for i in db_images:
            c[i.image_path] = i
        self._logger.info(f'initialized local cache with {len(c)} images')
        return c

    def _add_image(self, image_path: Path):
        image_path_str = image_path.__str__()
        self._logger.info(f'adding image {image_path_str} to DB')
        im = Image(
            image_path=image_path_str,
        )
        self._db.add_image_to_db(im)
        self._cache[image_path_str] = im

    def _remove_image(self, image: Image):
        self._logger.info(f'removing image {image.image_path} from DB')
        self._db.remove_image_from_db(image)
        del self._cache[image.image_path]
