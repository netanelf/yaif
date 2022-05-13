import logging
import time
from datetime import datetime

import configuration
from mysql_db import MySqlDb
from fs_monitor import FileSystemMonitor


def init_logging(level):
    root_logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(level)


def main():
    init_logging(logging.DEBUG)
    cfg = configuration.get_default_configuration()
    db = MySqlDb(cfg.images_db_file_path)
    mon = FileSystemMonitor(cfg=cfg, db=db)
    time.sleep(60*5)




if __name__ == '__main__':
    main()
