from dataclasses import dataclass


@dataclass
class Resolution:
    x: int
    y: int


@dataclass
class Image:
    image_path: str
    image_resolution: Resolution
