from jpegcompressor.jpegcompressor import compress
from jpegcompressor.helper import *

import numpy as np

path_grayscale_image = "./images/grayscale/Kodak08gray.bmp"


# bytearray
# result = compress(path_grayscale_image)


# store bytearry to file, then encode the file with other methods


def run():
    test_image = "images/test.bmp"
    compress(test_image)


if __name__ == '__main__':
    # check_steps()
    run()
