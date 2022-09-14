import threading
import os
from concurrent.futures import ThreadPoolExecutor, wait
from queue import Queue
from typing import List
from overlay_logo_py.image.logo import Overlay
from overlay_logo_py.handler import data


class Runner:
    __lock = threading.Lock() # might not need?
    __executor = ThreadPoolExecutor(max_workers=os.cpu_count() - 2)
    __tasks = list()
    queue = Queue(maxsize=1)
    __ui_thread = threading.Thread(target=print, args('UI thread not assigned.'), daemon=True)

    @property
    def ui_thread_running(self):
        return self.__ui_thread.is_alive()

    def start_ui_thread(self, ui) -> Queue:
        self.__ui_thread = threading.Thread(target=ui, args=(self.queue), daemon=True)
        self.__ui_thread.start()
        return self.queue
    
    def process_images(self, tasks: data.ImageTasks):
        for image in tasks.image_paths:
            # TODO: Still need to have something apply the save pattern to the save path, should probably redo the class in data
            self.__tasks.append(self.__executor.submit(Overlay.overlay, tasks.logo_path, image, tasks.position, tasks.save_dir + tasks.save_name))

