from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Resolution:
    x: int
    y: int


@dataclass
class Image:
    image_path: str
    image_resolution: Resolution
    view_count: int = field(default=0)
    last_view_ts: datetime = field(default=datetime.min)

