import PySimpleGUI as sg
import logging
import decimal
from decimal import Decimal

from overlay_logo_py.interface import ui
from overlay_logo_py.handler import data

sg.theme("DarkGrey1")
logger = logging.getLogger(__name__)


class OverlayUI:
    @staticmethod
    def start_event_loop(queue, debug: bool = True):

        window = sg.Window('Overlay Logo', ui.Layouts.layout, finalize=True)

        ratio = (0, 0)
        point = window['graph'].DrawPoint((0, 0), 8, color='red')
        xs = [x for x in range(0, window['graph'].CanvasSize[0]+1) if x % round(window['graph'].CanvasSize[0]/10) == 0]
        ys = [y for y in range(0, window['graph'].CanvasSize[1]+1) if y % round(window['graph'].CanvasSize[1]/10) == 0]
        for x in xs:
            window['graph'].draw_line((x, 0), (x, window['graph'].CanvasSize[1]))
        for y in ys:
            window['graph'].draw_line((0, y), (window['graph'].CanvasSize[0], y))

        logger.debug('Starting UI event loop')
        while True:
            event, values = window.read()

            logger.debug(f'{event}, {values}')

            if event in (None, 'Exit'):
                logger.debug('Exiting')
                queue.put(data.ExitEvent)
                break
            elif event == 'graph':
                graph_position = values['graph']
                graph = window['graph']
                ratio = (graph_position[0] / graph.CanvasSize[0], graph_position[1] / graph.CanvasSize[1])
                ratio = (Decimal(ratio[0]).quantize(Decimal('.0'), rounding=decimal.ROUND_HALF_UP), Decimal(ratio[1]).quantize(Decimal('.0'), rounding=decimal.ROUND_HALF_UP))
                pos = (int(graph.CanvasSize[0] * ratio[0]), int(graph.CanvasSize[1] * ratio[1]))
                graph.relocate_figure(point, pos[0] if pos[0] == 0 else pos[0] - 4, pos[1] if pos[1] == 0 else pos[1] - 4)
            elif event == 'run_overlay':
                image_paths = values['image_paths'].split(';')
                logo_path = values['logo_path']
                save_dir = values['save_path']
                save_pattern = values['save_pattern']
                if min(map(len, (image_paths, logo_path, save_dir, save_pattern))) == 0:
                    logger.warning('Input fields cannot be empty.')
                    continue
                image_list = list()
                for i in image_paths:
                    # TODO: redo logo overlay to take a ratio instead of absolute position
                    # TODO: ex. match 0.2*x on logo w/ 0.2*x on image (same with y)
                    image_list.append(data.ImageData(i, logo_path, POSITION, save_dir, save_pattern))
