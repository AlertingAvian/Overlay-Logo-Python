import logging
from typing import Tuple

import PIL
from PIL import Image

logger = logging.getLogger(__name__)


class Overlay:
    @staticmethod
    def __load_image(path) -> Image:
        try:
            image = Image.open(path)
        except Exception as e:
            if isinstance(e, FileNotFoundError) or isinstance(e, PIL.UnidentifiedImageError):
                # file doesn't exist or isn't an image
                logger.warning(f'Unable to find image at specified path -> {e}')
                raise e
            else:
                # other error, have to raise it myself because I didn't specify which error to catch.
                logger.error(e)
                raise e
        else:
            return image

    @staticmethod
    def overlay(logo_path: str, image_path: str, ratio: Tuple[int, int], save_path: str) -> str:
        """
        Overlay logo on image
        :param logo_path: Path to logo
        :param image_path: Path to Image
        :param ratio: I don't have a good way to describe it
        :param save_path: Where to save the image w/ file name
        :return: str, The path to the image. Not really needed
        :raises FileNotFoundError: The file doesn't exist (logo or image)
        :raises UnidentifiedImageError: The file isn't an image (logo or image)
        :raises ValueError: Position would place the logo outside the image
        """
        # load files
        logger.debug(f'image path: {image_path}')
        logger.debug(f'logo_path: {logo_path}')
        image = Overlay.__load_image(image_path)
        logo = Overlay.__load_image(logo_path)

        x_pos = (image.size[0] * ratio[0]) - (logo.size[0] * ratio[0])
        y_pos = (image.size[1] * ratio[1]) - (logo.size[1] * ratio[1])
        position = (int(x_pos), int(y_pos))
        logger.debug(position)

        # make sure position is in image
        bounds = image.size
        position_br = (position[0] + logo.size[0], position[1] + logo.size[1])
        if not position[0] in range(bounds[0] + 1) or not position[1] in range(bounds[1] + 1):
            logger.warning(f'Logo placed outside image or image is smaller than logo. Skipping {image_path}')
            raise Exception(f'Logo placed outside image or image is smaller than logo. Skipping {image_path}')
        if not position_br[0] in range(bounds[0] + 1) or not position_br[1] in range(bounds[1] + 1):
            logger.warning(f'Logo placed outside image or image is smaller than logo. Skipping {image_path}')
            raise Exception(f'Logo placed outside image or image is smaller than logo. Skipping {image_path}')
        del bounds
        del position_br

        # convert image to RGBA, paste logo on top
        image.convert("RGBA")
        image.paste(logo, position, mask=logo)

        logger.debug(f'Saving to: {save_path}')
        image.save(save_path)
        return save_path
