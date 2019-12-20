"""
Copyright (C) 2019 Patrick Maloney

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import PySimpleGUI as sg
import PIL.Image
import time # May not be needed after redesign

sg.change_look_and_feel('DefaultNoMoreNagging') # Yes I want the window to be a boring gray

###
# Settings Tab
###

layout_settings = [ # Place Holder Labels, Please Remember to rename
                    [sg.Text('Path of images:'), sg.InputText(), sg.FileBrowse()],
                    [sg.Text('Image to Overlay:'), sg.InputText(), sg.FileBrowse()],
                    [sg.Text('Where to save images:'), sg.InputText(), sg.FileBrowse()],
                    [sg.Text('Where to put the logo:'),sg.Radio('Top Left', 'locations', default=True), sg.Radio('Top Right', 'locations'), sg.Radio('Bottom Left', 'locations'), sg.Radio('Bottom Right', 'Locations')],
                    [sg.Button('Apply Settings')]
                    ]
tab_settings = [
                [sg.Frame('Settings', layout_settings, title_color='Blue')]
                ]

###
# Main Layout
###

layout = [
            [sg.TabGroup([[sg.Tab('Settings', tab_settings)]])],
            [sg.Exit()]
            ]

window = sg.Window('Overlay Logo', layout)

while True:
    event, values = window.read()

    # print(event, values) # Debug

    if event in (None, 'Exit'):
        break
