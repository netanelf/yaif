import logging
import tkinter as tk

import configuration
from mysql_db import MySqlDb
from fs_monitor import FileSystemMonitor
from image_list import ImageList
from display import Display
from screen_controller_10i import ScreenController10i


def init_logging(level):
    root_logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(level)
    logging.getLogger("PIL.PngImagePlugin").setLevel(logging.INFO)


def main():
    init_logging(logging.DEBUG)
    cfg = configuration.get_default_configuration()
    db = MySqlDb(cfg.images_db_file_path)
    mon = FileSystemMonitor(cfg=cfg, db=db)
    image_list = ImageList(db=db)
    screen_controller = ScreenController10i(configuration=cfg)
    display = Display(cfg, image_list, screen_controller)
    display.mainloop()




if __name__ == '__main__':
    main()
