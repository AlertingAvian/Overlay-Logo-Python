import PySimpleGUI as sg
from overlay_logo_py.interface import ui

sg.theme("DarkGrey1")


class OverlayUI:
    @staticmethod
    def start_event_loop(queue, debug: bool = False):
        
        window = sg.Window('Overlay Logo', ui.Layouts.layout)

        while True:
            event, values = window.read()

            if debug:
                print(event, values)

            if event in (None, 'Exit'):
                break

