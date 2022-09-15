from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Tuple
from uuid import uuid4


@dataclass
class ImageData:
    image_path: str
    logo_path: str
    position: Tuple[int, int]
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
            r'%YYYY': str(now.year)
        }

        file_name = self.save_pattern
        for pattern, result in patterns.items():
            file_name = file_name.replace(pattern, result)

        return str(Path(self.save_dir) / Path(file_name))


ExitEvent = object()
