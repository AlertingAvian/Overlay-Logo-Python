import decimal
import logging
from decimal import Decimal

import PySimpleGUI as sg

from handler import data
from interface import ui

sg.theme("DarkGrey1")
logger = logging.getLogger(__name__)


class OverlayUI:
    def __init__(self, out_queue):
        self.out_queue = out_queue
        self.window = None

    def start_event_loop(self):
        self.window = sg.Window('Overlay Logo', ui.Layouts.layout, finalize=True)
        # initialize graph things
        ratio = (0, 0)
        point = self.window['graph'].DrawPoint((0, 0), 8, color='red')

        xs = [x + 13 for x in range(0, self.window['graph'].CanvasSize[0] + 1) if
              x % round(self.window['graph'].CanvasSize[0] / 10) == 0]
        ys = [y + 10 for y in range(0, self.window['graph'].CanvasSize[1] + 1) if
              y % round(self.window['graph'].CanvasSize[1] / 10) == 0]
        for x in xs:
            self.window['graph'].draw_line((x, 0), (x, self.window['graph'].CanvasSize[1]))
        for y in ys:
            self.window['graph'].draw_line((0, y), (self.window['graph'].CanvasSize[0], y))

        x = int(self.window['graph'].CanvasSize[0] / 2)
        self.window['graph'].draw_line((x, 0), (x, self.window['graph'].CanvasSize[1]), color='lime green')
        y = int(self.window['graph'].CanvasSize[1] / 2)
        self.window['graph'].draw_line((0, y), (self.window['graph'].CanvasSize[0], y), color='lime green')

        logger.debug('Starting UI event loop')
        while True:
            event, values = self.window.read()

            logger.debug(f'{event}, {values}')

            if event in (None, 'Exit'):
                logger.debug('Exiting')
                break
            elif event == 'graph':
                graph_position = values['graph']
                graph = self.window['graph']
                ratio = (graph_position[0] / graph.CanvasSize[0], graph_position[1] / graph.CanvasSize[1])
                ratio = (Decimal(ratio[0]).quantize(Decimal('.0'), rounding=decimal.ROUND_HALF_UP),  # don't know why
                         Decimal(ratio[1]).quantize(Decimal('.0'), rounding=decimal.ROUND_HALF_UP))  # I'm using
                pos = (int(graph.CanvasSize[0] * ratio[0]), int(graph.CanvasSize[1] * ratio[1]))  # Decimal
                graph.relocate_figure(point, pos[0] if pos[0] == 0 else pos[0] - 4,
                                      pos[1] if pos[1] == 0 else pos[1] - 4)
                logger.debug(pos)
            elif event == 'run_overlay':
                logger.debug(f'ratio: {ratio}')
                image_paths = values['image_paths'].split(';')
                logo_path = values['logo_path']
                save_dir = values['save_dir']
                save_pattern = values['save_pattern']
                if min(map(len, (image_paths, logo_path, save_dir, save_pattern))) == 0:
                    logger.warning('Input fields cannot be empty.')
                    continue
                self.window['run_overlay'].update(disabled=True)
                self.window['run_overlay'].SetTooltip('Tasks already running.')
                self.window['bar'].update(0)
                image_list = list()
                ratio = (float(ratio[0]), float(ratio[1]))
                for i in image_paths:
                    image_list.append(data.ImageData(i, logo_path, ratio, save_dir, save_pattern))
                self.out_queue.put(image_list)

        self.out_queue.put(data.ExitEvent)
        self.window.close()

    def update_progress(self, progress):
        logger.debug(f'{progress}% complete')
        self.window['bar'].update(progress)
        if progress == 100:
            self.window['run_overlay'].update(disabled=False)
            self.window['run_overlay'].SetTooltip('')
