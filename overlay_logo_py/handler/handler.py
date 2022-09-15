import logging
import os
import threading
from concurrent.futures import ThreadPoolExecutor, wait
from queue import Queue
from typing import List

from overlay_logo_py.handler import data
from overlay_logo_py.image.logo import Overlay

logger = logging.getLogger(__name__)


class Runner:
    __lock = threading.Lock()  # might not need?
    __executor = ThreadPoolExecutor(max_workers=os.cpu_count())
    __tasks = list()
    queue = Queue(maxsize=1)
    __ui_thread = threading.Thread(target=logger.error, args=('UI thread not assigned.',), daemon=True)

    @property
    def ui_thread_running(self):
        return self.__ui_thread.is_alive()

    def start_ui_thread(self, ui) -> Queue:
        logger.info('Starting UI')
        self.__ui_thread = threading.Thread(target=ui, args=(self.queue,), daemon=True)
        self.__ui_thread.start()
        return self.queue

    def process_images(self, tasks: List[data.ImageData]):
        for image_data in tasks:
            self.__tasks.append(
                Overlay.overlay(image_data.logo_path, image_data.image_path, image_data.position, image_data.save_path))
        threading.Thread(target=self.__run_tasks, daemon=True).start()

    def __run_tasks(self):
        wait(self.__tasks)
