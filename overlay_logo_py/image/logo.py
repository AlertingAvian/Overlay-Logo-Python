import PIL
from PIL import Image
from typing import Tuple


class Overlay:
    @staticmethod
    def __load_image(path) -> Image:
        try:
            image = Image.open(path)
        except Exception as e:
            if isinstance(e, FileNotFoundError) or isinstance(e, PIL.UnidentifiedImageError):
                # file doesn't exist or isn't an image
                print(f'Unable to find image at specified path -> {e}')
                raise e
            else:
                # other error, have to raise it myself because I didn't specify which error to catch.
                raise e
        else:
            return image

    @staticmethod
    def overlay(logo_path: str, image_path: str, position: Tuple[int, int], save_path: str) -> str:
        """
        Overlay logo on image
        :param logo_path: Path to logo
        :param image_path: Path to Image
        :param position: Coord of image of where to place the logo
        :param save_path: Where to save the image w/ file name
        :return: str, The path to the image. Not really needed
        :raises FileNotFoundError: The file doesn't exist (logo or image)
        :raises UnidentifiedImageError: The file isn't an image (logo or image)
        :raises ValueError: Position would place the logo outside the image
        """
        # load files
        image = Overlay.__load_image(image_path)
        logo = Overlay.__load_image(logo_path)

        # make sure position is in image
        bounds = image.size
        position_br = (position[0] + logo.size[0], position[1] + logo.size[1])
        if not position[0] in range(bounds[0]+1) or not position[1] in range(bounds[1]+1):
            raise ValueError(f'Specified position: {position} out of bounds: {bounds}')
        if not position_br[0] in range(bounds[0]+1) or not position_br[1] in range(bounds[1]+1):
            raise ValueError(f'Specified position bottom right: {position_br} out of bounds: {bounds}')
        del bounds

        # convert image to RGBA, paste logo on top
        image.convert("RGBA")
        image.paste(logo, position + position_br, mask=logo)

        image.save(save_path)
        return save_path

