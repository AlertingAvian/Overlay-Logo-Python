import PySimpleGUI as sg

class Layouts:
    layout_settings = [
            [sg.Text("Images:"), sg.InputText(key="image_paths"), sg.FilesBrowse()],
            [sg.Text("Logo:"), sg.InputText(key="logo_path"), sg.FileBrowse()],
            [sg.Text("Save Directory:"), sg.InputText(key="save_path"), sg.FolderBrowse()],
            [sg.Text("Save Pattern:"), sg.InputText(key="save_pattern"), sg.Button('Apply', key='apply-pattern')],
            [sg.Text("--Pattern information here--")]  # see data.py for pattern
            # need selection for logo location
    ]
    tab_settings = [
        [sg.Frame('Settings', layout_settings)]
    ]

    layout_run = [
        [sg.Button('Run', key="run_overlay")]
        # need more things here
        # console output
        # progress bar
    ]
    tab_run = [
        [sg.Frame("Run", layout_run)]
    ]

    layout = [
        [sg.TabGroup([[sg.Tab('Settings', tab_settings), sg.Tab('Run', tab_run)]])],
        [sg.Exit()]
    ]
