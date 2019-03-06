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

import tkinter as tki
from tkinter import filedialog, messagebox
from pathlib import Path
from pathlib import PurePath
import PIL.Image
import time
import PrintTags as pt



# Init Vars
product_files = []
logo_file = None
product_path = None
product_path_old = None
modified_path = None

root = tki.Tk()
root.title("Logo Overlayer")
root.geometry("600x125")
root.resizable(width=True,height=False)

# Path selection functions

def choose_logo():
    global logo_file
    logo_file = filedialog.askopenfilename(initialdir=".",title="Select Logo",filetypes=(("png files","*.png"),("all files","*.*")))
    if len(logo_file) == 0:
        pt.warn("No file selected.")
        return
    logo_label.config(text=str(logo_file))
    pt.info("Selected: " + logo_file)

def choose_product_path():
    global product_path
    product_path = filedialog.askdirectory(initialdir=".",title="Select Folder With Product Images")
    if len(product_path) == 0:
        pt.warn("No file selected.")
        return
    product_label.config(text=str(product_path))
    pt.info("Selected: " + product_path)

def choose_modified_path():
    global modified_path
    modified_path = filedialog.askdirectory(initialdir=".",title="Select Folder To Save Images")
    if len(modified_path) == 0:
        pt.warn("No file selected.")
        return
    modified_label.config(text=str(modified_path))
    pt.info("Selected: " + modified_path)

""" START: IMAGE PASTING """
def add_logo_tl():
    global logo_file, modified_path, product_files
    logo = PIL.Image.open(logo_file)
    for file in product_files:
        img = PIL.Image.open(file)
        img.convert("RGBA")
        left = 0
        upper = 0
        right = logo.size[0]
        lower = logo.size[1]
        img.paste(logo, (left, upper, right, lower), mask=logo)
        path = Path("{0}_with_logo_tl-{1}.png".format(file.stem,time.time()))
        save_path = Path(modified_path).joinpath(path)
        img.save(save_path)
        pt.info("Saved: " + str(path))
    pt.success("Saved all loaded images.")
    messagebox.showinfo("Complete","Images saved")


def add_logo_bl():
    global logo_file, modified_path, product_files
    logo = PIL.Image.open(logo_file)
    for file in product_files:
        img = PIL.Image.open(file)
        img.convert("RGB")
        left = 0
        upper = img.size[1] - logo.size[1]
        right = logo.size[0]
        lower = img.size[1]
        img.paste(logo, (left, upper, right, lower), mask=logo)
        path = Path("{0}_with_logo_bl-{1}.png".format(file.stem,time.time()))
        save_path = Path(modified_path).joinpath(path)
        img.save(save_path)
        pt.info("Saved: " + str(path))
    pt.success("Saved all loaded images.")
    messagebox.showinfo("Complete","Images saved")


def add_logo_tr():
    global logo_file, modified_path, product_files
    logo = PIL.Image.open(logo_file)
    for file in product_files:
        img = PIL.Image.open(file)
        img.convert("RGBA")
        left = img.size[0] - logo.size[0]
        upper = 0
        right = img.size[0]
        lower = logo.size[1]
        img.paste(logo, (left, upper, right, lower), mask=logo)
        path = Path("{0}_with_logo_tr-{1}.png".format(file.stem,time.time()))
        save_path = Path(modified_path).joinpath(path)
        img.save(save_path)
        pt.info("Saved: " + str(path))
    pt.success("Saved all loaded images.")
    messagebox.showinfo("Complete","Images saved")


def add_logo_br():
    global logo_file, modified_path, product_files
    logo = PIL.Image.open(logo_file)
    for file in product_files:
        img = PIL.Image.open(file)
        img.convert("RGBA")
        left = img.size[0] - logo.size[0]
        upper = img.size[1] - logo.size[1]
        right = img.size[0]
        lower = img.size[1]
        img.paste(logo, (left, upper, right, lower), mask=logo)
        path = Path("{0}_with_logo_br-{1}.png".format(file.stem,time.time()))
        save_path = Path(modified_path).joinpath(path)
        img.save(save_path)
        pt.info("Saved: " + str(path))
    pt.success("Saved all loaded images.")
    messagebox.showinfo("Complete","Images saved")


""" END IMAGE PASTING """

def ask_loc():
    top = tki.Toplevel()
    top.title("Select a postition")
    top.resizable(width=False,height=False)
    top.geometry("165x100+400+400")
    tl_bn = tki.Button(top,text="Top Left",command=add_logo_tl)
    tl_bn.grid(row=0,column=0)
    bl_bn = tki.Button(top,text="Bottom Left",command=add_logo_bl)
    bl_bn.grid(row=1,column=0)
    tr_bn = tki.Button(top,text="Top Right",command=add_logo_tr)
    tr_bn.grid(row=0,column=1)
    br_bn = tki.Button(top,text="Bottom Right",command=add_logo_br)
    br_bn.grid(row=1,column=1)
    done_bn = tki.Button(top,text="DONE",command=top.destroy)
    done_bn.grid(row=2,column=0,columnspan=2)


def start():
    global logo_file, product_path, modified_path, product_files, product_path_old
    if logo_file == None or product_path == None or modified_path == None:
        pt.warn("You must select a logo, a path for your products, and a path the output the pictures.")
        messagebox.showwarning("Warning","You must select a logo, a path for your products, and a path the output the pictures.")
        return
    else:
        pl_product_path = Path(product_path)
        if product_path_old != pl_product_path:
            for file in pl_product_path.iterdir():
                if file.suffix == '.png' or file.suffix == '.jpg':
                    product_files.append(file)
            product_path_old = pl_product_path
        if len(product_files) == 0:
            pt.warn("Path contained no images.")
            messagebox.showwarning("Warning","Product path contained no images.")
            return
        else:
            # load_bn['state']= 'disabled'
            ask_loc()

# ROOT Path selection buttons and labels
logo_bn = tki.Button(root, text="Select Logo",command=choose_logo)
product_path_bn = tki.Button(root, text="Select Product Image Path",command=choose_product_path)
final_path_bn = tki.Button(root, text="Select Modified Image Path",command=choose_modified_path)
logo_bn.grid(column=0,row=0)
product_path_bn.grid(column=0,row=1)
final_path_bn.grid(column=0,row=2)

logo_label = tki.Label(root,text="None")
product_label = tki.Label(root,text="None")
modified_label = tki.Label(root,text="None")
logo_label.grid(column=1,row=0)
product_label.grid(column=1,row=1)
modified_label.grid(column=1,row=2)

load_bn = tki.Button(root,text="Load Images",command=start)
load_bn.grid(column=0,row=3)

root.mainloop()
