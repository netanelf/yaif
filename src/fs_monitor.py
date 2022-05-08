from configuration import Configuration
from db_base import DbBase


class FileSystemMonitor:
    def __init__(self, cfg: Configuration, db: DbBase):
        self._cfg = cfg
        self._db = db

    def run(self):
        # monitor files in paths (cfg)
        # add/ remove from db using db
        pass