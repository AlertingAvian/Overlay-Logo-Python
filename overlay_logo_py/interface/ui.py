import PySimpleGUI as sg

sg.theme("DarkGrey1")


class OverlayUI:
    @staticmethod
    def start_event_loop():
        layout_settings = [
            [sg.Text("Images:"), sg.InputText(), sg.FilesBrowse()],
            [sg.Text("Logo:"), sg.InputText(), sg.FileBrowse()],
            [sg.Text("Save Location"), sg.InputText(), sg.FilesBrowse()],
            # need selection for logo location
        ]
        tab_settings = [
            [sg.Frame('Settings', layout_settings)]
        ]
        # need to go and switch ' with "
        layout_run = [
            [sg.Button('Run')]
            # need more things here
        ]
        tab_run = [
            [sg.Frame("Run", layout_run)]
        ]

        layout = [
            [sg.TabGroup([[sg.Tab('Settings', tab_settings), sg.Tab('Run', tab_run)]])],
            [sg.Exit()]
        ]
        window = sg.Window('Overlay Logo', layout)

        while True:
            event, values = window.read()

            print(event, values)

            if event in (None, 'Exit'):
                break
