import logging
import sys

from handler import data
from handler.handler import Runner
from interface.ui_runner import OverlayUI


def main():
    logging.basicConfig(handlers=[
        logging.FileHandler('overlay.log'),
        logging.StreamHandler(sys.stdout)
    ], level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.debug('Initializing Runner')
    runner = Runner()

    logger.info('Starting main loop')

    queue = runner.start_ui_thread(OverlayUI.start_event_loop)
    while True:
        if not queue.empty():
            from_ui = queue.get(timeout=5)
            if from_ui is data.ExitEvent:
                logger.info('Received ExitEvent from ui runner')
                break
            elif len(from_ui) != 0 and isinstance(from_ui, list):
                if isinstance(from_ui[0], data.ImageData):
                    runner.process_images(from_ui)
                else:
                    logger.warning(f'List from UI is not an instance of data.ImageData -> {type(from_ui[1])}')

    logger.info('Exiting')


if __name__ == '__main__':
    main()
