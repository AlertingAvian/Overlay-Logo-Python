from dataclasses import dataclass
from typing import List, Tuple
from pathlib import Path
from datetime import datetime
from uuid import uuid4

@dataclass
class ImageTasks:
    # might need to make a more granular one where
    # the image, logo, and position are their own class
    # to allow for independent logos and positions for each image
    image_paths: List[str],
    logo_path: str,
    save_dir: str,
    save_name: str,
    position: Tuple[int, int]



@dataclass
class Image:
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
            r'%UUID': str(uuid4()),
            r'%DD': str(now.day),
            r'%MM': str(now.month) if len(str(now.month)) == 2 else "0" + str(now.month),
            r'%YYYY': str(now.year)
        }

        fname = self.save_pattern
        for pattern, result in patterns.items():
            fname = replace(pattern, result)
        
        return str(Path(self.save_dir) / Path(fname))
    