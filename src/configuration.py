from dataclasses import dataclass, field
from typing import List


########################################### DEFAULT CONFIGURATION  #####################################################
IMAGE_DIRS = [
    r'/home/netanel/Pictures',
]

########################################################################################################################


@dataclass
class Configuration:
    image_dirs: List[str]
    display_time_sec: int = field(default=10)


def get_default_configuration():
    c = Configuration(
        image_dirs=IMAGE_DIRS
    )

    return c
