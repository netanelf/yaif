from dataclasses import dataclass, field
from typing import List, Tuple


########################################### DEFAULT CONFIGURATION  #####################################################
IMAGE_DIRS = [
    r'/home/netanel/Pictures',
]

DB_PATH = 'images.db'
RUN_FULLSCREEN = True

########################################################################################################################


@dataclass
class Configuration:
    image_dirs: List[str]
    images_db_file_path: str
    display_time_sec: int = field(default=10)
    supported_image_extensions: List[str] = field(default_factory=lambda: ['png', 'jpg'])
    periodic_monitor_freq_sec: int = field(default=60)
    screen_size: Tuple[int] = field(default_factory=lambda: (1080, 1920))  #h, w
    run_true_fullscreen: bool = field(default=False)


def get_default_configuration():
    c = Configuration(
        image_dirs=IMAGE_DIRS,
        images_db_file_path=DB_PATH,
        run_true_fullscreen=RUN_FULLSCREEN
    )
    return c
