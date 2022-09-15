import PySimpleGUI as sg


class Layouts:
    layout_settings = [
        [sg.Text("Images:"), sg.InputText(key="image_paths"), sg.FilesBrowse()],
        [sg.Text("Logo:"), sg.InputText(key="logo_path"), sg.FileBrowse()],
        [sg.Text("Save Directory:"), sg.InputText(key="save_dir"), sg.FolderBrowse()],
        [sg.Text("Save Pattern:"), sg.InputText(key="save_pattern", default_text='%F_%L'),
         sg.Button('Apply', key='apply-pattern')],
        [sg.Text("--Pattern information here--")],  # see data.py for pattern
        # need selection for logo location
        [sg.Graph(canvas_size=(250, 200), graph_bottom_left=(0, 200), graph_top_right=(250, 0), background_color='grey', key='graph', enable_events=True)]
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
