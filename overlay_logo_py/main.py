import logging
import sys

from overlay_logo_py.handler import data
from overlay_logo_py.handler.handler import Runner
from overlay_logo_py.interface.ui_runner import OverlayUI

"""
main -handler-> start ui (loop)
handler -> queue -> main
main -> listens to queue for data
ui loop -queue-> sends task data (image path list, logo path, save path) -> main
main -> list of image paths, logo path, save path, (other info) -> ThreadPool runner
ThreadPool runner (running on main thread) (might want to move to new thread)-> splits up images to threadpool to process (threads spawned from pool on own thread)
??? -> image completion reported to ui for progress bar
"""


def main():
    logging.basicConfig(handlers=[
        logging.FileHandler('overlay.log'),
        logging.StreamHandler(sys.stdout)
    ], level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger.debug('Initializing Runner')
    runner = Runner()
    logger.debug('Starting main loop')

    queue = runner.start_ui_thread(OverlayUI.start_event_loop)
    while True:
        if not queue.empty():
            from_ui = queue.get(timeout=5)
            if from_ui is data.ExitEvent:
                logger.info('Received ExitEvent from ui runner')
                break
            else:
                print(from_ui)
    logger.info('Exiting')


if __name__ == '__main__':
    main()
