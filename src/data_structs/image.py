from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Image:
    image_path: str
    view_count: int = field(default=0)
    last_view_ts: datetime = field(default=datetime.min)
    do_not_show_image: bool = field(default=False)
    comment: str = field(default='')

