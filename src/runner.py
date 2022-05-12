import logging
from datetime import datetime

import configuration
from mysql_db import MySqlDb
from data_structs.image import Image, Resolution


def init_logging(level):
    root_logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(level)


def main():
    init_logging(logging.DEBUG)
    c = configuration.get_default_configuration()
    db = MySqlDb(c.images_db_file_path)
    # db.add_image_to_db(Image(
    #     image_path='12345',
    #     image_resolution=Resolution(2,6),
    # ))
    ims = db.get_all_images_in_db()
    print(ims)
    print(db.update_image_view_count(ims[0]))
    db.update_image_last_view_timestamp(ims[0], datetime.now())



if __name__ == '__main__':
    main()
