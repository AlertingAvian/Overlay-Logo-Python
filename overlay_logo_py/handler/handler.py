import logging
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import List

from handler import data
from image.logo import Overlay
from interface.ui_runner import OverlayUI

logger = logging.getLogger(__name__)


class Runner:
    __lock = threading.Lock()  # might not need?
    __executor = ThreadPoolExecutor(max_workers=os.cpu_count())
    __ui_queue = Queue(maxsize=1)
    __ui_thread = threading.Thread(target=logger.error, args=('UI thread not assigned.',), daemon=True)
    __ui_runner = OverlayUI(__ui_queue)
    __num_tasks = int()
    __tasks_complete = int()

    @property
    def ui_thread_running(self):
        return self.__ui_thread.is_alive()

    def start_ui_thread(self, ui) -> Queue:
        logger.info('Starting UI')
        self.__ui_thread = threading.Thread(target=self.__ui_runner.start_event_loop, daemon=True)
        self.__ui_thread.start()
        return self.__ui_queue

    def process_images(self, tasks: List[data.ImageData]):
        logger.info('Starting tasks')
        self.__num_tasks = len(tasks)
        self.__tasks_complete = 0
        self.__run_tasks(tasks)
        # threading.Thread(target=self.__run_tasks, args=(tasks,), daemon=True).start()

    def __run_tasks(self, tasks):
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = [executor.submit(Overlay.overlay, x.logo_path, x.image_path, x.ratio, x.save_path) for x in tasks]

            for future in futures:
                future.add_done_callback(self.__tasks_progress)
        logger.info('Tasks completed')

    def __tasks_progress(self, future):
        if future.cancelled():
            logger.debug(f'Future cancelled: {future}')
        elif future.exception():
            logger.warning(f'Future completed with exception: {future}')
            # TODO: add in notification on run tab for skipped files
        else:
            logger.debug(f'Completed future: {future}')
        self.__tasks_complete += 1
        self.__ui_runner.update_progress(round((self.__tasks_complete / self.__num_tasks) * 100))
