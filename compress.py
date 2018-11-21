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


def check_steps():
    block = np.array([
        52, 55, 61, 66, 70, 61, 64, 73,
        63, 59, 55, 90, 109, 85, 69, 72,
        62, 59, 68, 113, 144, 104, 66, 73,
        63, 58, 71, 122, 154, 106, 70, 69,
        67, 61, 68, 104, 126, 88, 68, 70,
        79, 65, 60, 70, 77, 68, 58, 75,
        85, 71, 64, 59, 55, 61, 65, 83,
        87, 79, 69, 68, 65, 76, 78, 94
    ])

    block = block.reshape((8, 8))

    block -= 128
    block = DCT(block)
    block = quantization(block)
    array = zigzag(block)

    result = encode_coefficient(array, 0)

    decode_array = decode_coefficient(result, 0)


if __name__ == '__main__':
    check_steps()
    run()
