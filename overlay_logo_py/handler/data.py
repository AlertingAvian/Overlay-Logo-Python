from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Tuple
from uuid import uuid4


@dataclass
class ImageData:
    image_path: str
    logo_path: str
    ratio: Tuple[float, float]
    save_dir: str
    save_pattern: str

    @property
    def save_path(self):
        now = datetime.now()
        patterns = {
            r'%F': Path(self.image_path).stem,
            r'%L': Path(self.logo_path).stem,
            r'%UUID': str(uuid4()),
            r'%DD': str(now.day) if len(str(now.day)) == 2 else "0" + str(now.day),
            r'%MM': str(now.month) if len(str(now.month)) == 2 else "0" + str(now.month),
            r'%YYYY': str(now.year),
            r'%YY': str(now.year)[2:]
        }

        file_name = self.save_pattern
        for pattern, result in patterns.items():
            file_name = file_name.replace(pattern, result)

        if Path(file_name).suffix == '' or not Path(file_name).suffix.lower() in (
                ".png", ".jpeg", ".jpg", ".ppm", ".gif", ".tiff", ".bmp"):
            file_name += '.png'

        return str(Path(self.save_dir) / Path(file_name))


ExitEvent = object()
TaskComplete = object()
