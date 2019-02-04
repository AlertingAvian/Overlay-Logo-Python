import PIL.Image
import sys
import time
from pathlib import Path

# Save paths
picture_path = Path(".\Pictures")
logo_path = Path(".\Pictures\Logos")
product_path = Path(".\Pictures\Product_Pictures")
modified_imgs = Path(".\Pictures\Modified_Images")

# Init lists
logo_images = []
logo_filenames = []
product_images = []
product_filenames = []


def create_dirs():
    if not picture_path.exists():
        picture_path.mkdir()
        print("{} Path Created".format(picture_path))
    if not logo_path.exists():
        logo_path.mkdir()
        print("{} Path Created".format(logo_path))
    if not product_path.exists():
        product_path.mkdir()
        print("{} Path Created".format(product_path))
    if not modified_imgs.exists():
        modified_imgs.mkdir()
        print("{} Path Created".format(modified_imgs))


def load_images():
    run = False
    for product_file in product_path.iterdir():
        if product_file.suffix == ".jpg" or product_file.suffix == ".png":
            product_images.append(product_file)
            product_filenames.append(product_file.stem)
    for logo_file in logo_path.iterdir():
        if logo_file.suffix == ".png":
            logo_images.append(logo_file)
            logo_filenames.append(logo_file.stem)
        elif logo_file.suffix == ".jpg" and run == False:
            run = True
            print()
            print("Logo images must be in the \".png\" image format. Skipping logos in the \".jpg\" format.")
            print()


def add_logo_tl(logo):
    for file in product_images:
        img = PIL.Image.open(file)
        print("Loaded: {}".format(file))
        img.convert("RGBA")
        left = 0
        upper = 0
        right = logo.size[0]
        lower = logo.size[1]
        img.paste(logo, (left, upper, right, lower), mask=logo)
        save_path = Path(".\Pictures\Modified_Images\{0}_with_logo_tl-{1}.png".format(file.stem,time.time()))
        img.save(save_path)
        print("Saved: {0}_with_logo_tl-{1}.png".format(file.stem,time.time()))
        print()


def add_logo_bl(logo):
    for file in product_images:
        img = PIL.Image.open(file)
        print("Loaded: {}".format(file))
        img.convert("RGBA")
        left = 0
        upper = img.size[1] - logo.size[1]
        right = logo.size[0]
        lower = img.size[1]
        img.paste(logo, (left, upper, right, lower), mask=logo)
        save_path = Path(".\Pictures\Modified_Images\{0}_with_logo_bl-{1}.png".format(file.stem,time.time()))
        img.save(save_path)
        print("Saved: {0}_with_logo_bl-{1}.jpg".format(file.stem,time.time()))
        print()


def add_logo_tr(logo):
    for file in product_images:
        img = PIL.Image.open(file)
        print("Loaded: {}".format(file))
        img.convert("RGBA")
        left = img.size[0] - logo.size[0]
        upper = 0
        right = img.size[0]
        lower = logo.size[1]
        img.paste(logo, (left, upper, right, lower), mask=logo)
        save_path = Path(".\Pictures\Modified_Images\{0}_with_logo_tr-{1}.png".format(file.stem,time.time()))
        img.save(save_path)
        print("Saved: {0}_with_logo_tr-{1}.png".format(file.stem,time.time()))
        print()


def add_logo_br(logo):
    for file in product_images:
        img = PIL.Image.open(file)
        print("Loaded: {}".format(file))
        img.convert("RGBA")
        left = img.size[0] - logo.size[0]
        upper = img.size[1] - logo.size[1]
        right = img.size[0]
        lower = img.size[1]
        img.paste(logo, (left, upper, right, lower), mask=logo)
        save_path = Path(".\Pictures\Modified_Images\{0}_with_logo_br-{1}.png".format(file.stem,time.time()))
        img.save(save_path)
        print("Saved: {0}_with_logo_br-{1}.png".format(file.stem,time.time()))
        print()


print("Checking Files...")
# Create Directories if they do not already exist. (see line 19)
create_dirs()
# Load Logos And Product Pictures (see line 34)
load_images()

# Test to see if there is any item in the logos and products Directories
if len(logo_images) == 0 and len(product_images) == 0:
    print("Add Logo Images and Product Images in their respective folders.")
    sys.exit()
elif len(logo_images) == 0:
    print("Add Logo Images to .\Pictures\Logos")
    sys.exit()
elif len(product_images) == 0:
    print("Add Product Images to .\Pictures\Product_Pictures")
    sys.exit()
else:
    print("File Check Complete.")
    print()

# Logo Selection
while True:
    continue0_0 = True
    continue0_1 = True
    print("Choose A Logo To Use:")
    count = 0
    for item in logo_filenames:
        count += 1
        print("{0}: {1}".format(count,item))
    try:
        logo_input = int(input())
    except ValueError:
        print("Input a number.")
        print()
        continue0_0 = False
        continue0_1 = False
    if continue0_0:
        try:
            active_logo_path = logo_images[logo_input-1]
        except IndexError:
            print("Selected Logo Is Not Avalible.")
            print()
            continue0_1 = False
    if continue0_1:
        active_logo = PIL.Image.open(active_logo_path)
        if active_logo.mode != "RGBA":
            print("Logos must have transparency. Stopping...")
            sys.exit()
        break

# Location Selection
while True:
    continue1_0 = True
    print("Select The Location To Put Your Logo:")
    print("1: Top Left")
    print("2: Bottom Left")
    print("3: Top Right")
    print("4: Bottom Right")
    try:
        location_input = int(input())
    except ValueError:
        print("Input A Number.")
        print()
        continue1_0 = False
    if continue1_0:
        if location_input in range(1,5):
            active_location = location_input
            break
        else:
            print("Selected Location Not Avalible.")
            print()

print("Adding Logo To Pictures...")
print()

# Calls the approprite function for the selected location (lines 51-112)
if active_location == 1:
    # top left
    add_logo_tl(active_logo)
if active_location == 2:
    # bottom left
    add_logo_bl(active_logo)
if active_location == 3:
    # top right
    add_logo_tr(active_logo)
if active_location == 4:
    # bottom left
    add_logo_br(active_logo)


print("Operation Complete.")

"""
Copyright 2019 Patrick Maloney

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
