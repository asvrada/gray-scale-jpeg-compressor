import numpy as np

from jpegcompressor.helper import *
from jpegcompressor.main import *


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

    original = block.copy()

    block -= 128
    block = DCT(block)
    block = quantization(block)
    array = zigzag(block)

    result = encode_coefficient(array, 0)

    _, decode_array = decode_coefficient(result, 0)
    decode_block = reverse_zigzag(decode_array)
    decode_block = reverse_quantization(decode_block)
    decode_block = iDCT(decode_block)
    decode_block += 128

    print(original - decode_block)


if __name__ == '__main__':
    # check_steps()
    test_image = "images/test.bmp"
    result = compress(test_image)

    result = decompress("", result)
    print(result)
