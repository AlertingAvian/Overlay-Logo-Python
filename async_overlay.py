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
import pathlib as pl
import PIL.Image
import time
import asyncio

# initialize variables to nonetype
pic_path = None
logo_path = None
save_path = None
logo_loc =  'tl' # location key- tl: top left, tr: top right, bl: bottom left, br: bottom right - top left is default

async def overlay(logo, logo_loc, save_path):
    print('HERE')
    for file in pic_path.iterdir():
        if file.suffix in ('.png','.jpg'):
            img = PIL.Image.open(file)
            img.convert("RGBA")
            if logo_loc == 'tl':
                left = 0
                upper = 0
                right = logo.size[0]
                lower = logo.size[1]
            elif logo_loc == 'tr':
                left = img.size[0] - logo.size[0]
                upper = 0
                right = img.size[0]
                lower = logo.size[1]
            elif logo_loc == 'bl':
                left = 0
                upper = img.size[1] - logo.size[1]
                right = logo.size[0]
                lower = img.size[1]
            elif logo_loc == 'br':
                left = img.size[0] - logo.size[0]
                upper = img.size[1] - logo.size[1]
                right = img.size[0]
                lower = img.size[1]
            img.paste(logo, (left, upper, right, lower), mask=logo)
            img_save = pl.Path(f'{file.stem}_with_logo--{time.time()}.png')
            img_path = save_path.joinpath(img_save)
            img.save(img_path)
            print(f'[INF]  Saved: {img_path}')
    print('[INF]  COMPLETE.')
    sg.PopupOK('Overlay Complete.','Images Saved')

sg.change_look_and_feel('DefaultNoMoreNagging') # Yes I want the window to be a boring gray

###
# Settings Tab
###

layout_settings = [ # Place Holder Labels, Please Remember to rename
                    [sg.Text('Path of images:'), sg.InputText(), sg.FolderBrowse()],
                    [sg.Text('Image to Overlay:'), sg.InputText(), sg.FileBrowse()],
                    [sg.Text('Where to save images:'), sg.InputText(), sg.FolderBrowse()],
                    [sg.Text('Where to put the logo:'),sg.Radio('Top Left', 'locations', default=True), sg.Radio('Top Right', 'locations'), sg.Radio('Bottom Left', 'locations'), sg.Radio('Bottom Right', 'locations')],
                    [sg.Button('Apply Settings')]
                    ]
tab_settings = [
                [sg.Frame('Settings', layout_settings, title_color='Blue')]
                ]

###
# Run Tab
###

layout_run = [
                [sg.Button('Start')],
                [sg.Text('Output:',text_color='Blue')],
                [sg.Output(size=(70,20))]
                ]
tab_run = [
            [sg.Frame('Run', layout_run, title_color='Blue')]
            ]

###
# Main Layout
###

layout = [
            [sg.TabGroup([[sg.Tab('Settings', tab_settings), sg.Tab('Run', tab_run)]])],
            [sg.Exit()]
            ]

window = sg.Window('Overlay Logo', layout)

async def overlay(logo, logo_loc, save_path):
    for file in pic_path.iterdir():
        if file.suffix in ('.png','.jpg'):
            img = PIL.Image.open(file)
            img.convert("RGBA")
            if logo_loc == 'tl':
                left = 0
                upper = 0
                right = logo.size[0]
                lower = logo.size[1]
            elif logo_loc == 'tr':
                left = img.size[0] - logo.size[0]
                upper = 0
                right = img.size[0]
                lower = logo.size[1]
            elif logo_loc == 'bl':
                left = 0
                upper = img.size[1] - logo.size[1]
                right = logo.size[0]
                lower = img.size[1]
            elif logo_loc == 'br':
                left = img.size[0] - logo.size[0]
                upper = img.size[1] - logo.size[1]
                right = img.size[0]
                lower = img.size[1]
            img.paste(logo, (left, upper, right, lower), mask=logo)
            img_save = pl.Path(f'{file.stem}_with_logo--{time.time()}.png')
            img_path = save_path.joinpath(img_save)
            img.save(img_path)
            print(f'[INF]  Saved: {img_path}')
    print('[INF]  COMPLETE.')
    sg.PopupOK('Overlay Complete.','Images Saved')

async def main():
    global pic_path, logo_path, save_path, logo_loc
    while True:
        event, values = window.read()

        # print(event, values) # Debug

        if event in (None, 'Cancel'):
            break

        elif event == 'Exit':
            if sg.PopupYesNo('Are you sure you want to exit?') == 'Yes':
                break

        elif event == 'Apply Settings':
            # Save settings to respective variables for ease of access
            pic_path = pl.Path(values['Browse'])
            logo_path = pl.Path(values['Browse0'])
            if logo_path.suffix != '.png':
                sg.PopupError('Invalid logo type. Please select a \'.png\' or \'.jpg\' file.')
                logo_path = None
            save_path = pl.Path(values['Browse1'])
            if pic_path == save_path: # Cannot save to the path being read: show error, set conflicts to nonetype
                sg.PopupError('Picture Path and Save Path cannot be the same.')
                pic_path = None
                save_path = None
                print('[ERR]  Paths set incorrectly')
            else:
                print(f'[INF]  Picture path set to: {pic_path}\n[INF]  Logo path set to: {logo_path}\n[INF]  Save path set to: {save_path}')
                if values[3]: # logo_loc key line 25
                    logo_loc = 'tl'
                    print('[INF]  Logo location set to: Top Left')
                elif values[4]:
                    logo_loc = 'tr'
                    print('[INF]  Logo location set to: Top Right')
                elif values[5]:
                    logo_loc = 'bl'
                    print('[INF]  Logo location set to: Bottom Left')
                elif values[6]:
                    logo_loc = 'br'
                    print('[INF]  Logo location set to: Bottom Right')
            print()

        elif event == 'Start':
            if pic_path and logo_path and save_path:
                logo = PIL.Image.open(logo_path)
                asyncio.ensure_future(overlay(logo, logo_loc, save_path))
                print('[INF]  Starting...\n')
            else:
                print('[ERR]  Settings Invalid')
                sg.PopupError('Your settings are invalid, please check them again and press Apply.')
            print()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    pending = asyncio.Task.all_tasks()
    loop.run_until_complete(asyncio.gather(*pending))
