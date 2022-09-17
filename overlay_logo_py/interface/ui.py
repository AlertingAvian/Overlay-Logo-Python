import PySimpleGUI as sg


class Layouts:
    graph_column = [
        [sg.Graph(canvas_size=(250, 200), graph_bottom_left=(0, 200), graph_top_right=(250, 0), background_color='grey',
                  key='graph', enable_events=True)]
    ]
    layout_settings = [
        [sg.Text("Images:"), sg.InputText(key="image_paths"), sg.FilesBrowse()],
        [sg.Text("Logo:"), sg.InputText(key="logo_path"), sg.FileBrowse()],
        [sg.Text("Save Directory:"), sg.InputText(key="save_dir"), sg.FolderBrowse()],
        [sg.Text("Save Pattern:"), sg.InputText(key="save_pattern", default_text='%F_%L')],
        [sg.Text("Save name pattern format:")],
        [sg.Text("%F", text_color='red'), sg.Text("for the image file name")],
        [sg.Text("%L", text_color='red'), sg.Text("for the logo file name")],
        [sg.Text("%DD", text_color='red'), sg.Text("for 2 character day")],
        [sg.Text("%MM", text_color='red'), sg.Text("for 2 character month")],
        [sg.Text("%YY", text_color='red'), sg.Text("for 2 character year")],
        [sg.Text("%YYYY", text_color='red'), sg.Text("for 4 character year")],
        [sg.Text("%UUID", text_color='red'), sg.Text("for a unique identifier (same UUID for all in current job)")],
        [sg.Text("Logo Anchor:")],
        [sg.Column(graph_column, element_justification='center', justification='center')]
    ]
    tab_settings = [
        [sg.Frame('Settings', layout_settings)]
    ]

    layout_run = [
        [sg.Button('Run', key="run_overlay")],
        [sg.ProgressBar(100, orientation='h', size=(45, 20), key='bar')],
        [sg.Text('If there are missing files check the log, a logo image may have been to large.',
                 background_color='red', text_color='white')]
    ]
    tab_run = [
        [sg.Frame("Run", layout_run, size=(500, 590))]
    ]

    layout = [
        [sg.TabGroup([[sg.Tab('Settings', tab_settings), sg.Tab('Run', tab_run)]])],
        [sg.Exit()]
    ]
