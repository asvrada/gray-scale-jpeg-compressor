from bitarray import bitarray

from .config import *
from .helper import *


# Entry for Compression
def compress(path_image, block_size=8):
    """
    Compress a grayscale image, return the result after transform but do not encode them

    The returned result has following structure:

    header: height, width, number of color channel
    body: compressed image

    :param path_image: path to the image
    :type path_image: str
    :param block_size: size of the DCT block, could be 8(8x8) or 16(16x16)
    :type block_size int
    :return: compressed image
    :rtype: bitarray
    """
    pix, im = load_image(path_image)

    result = bitarray()

    # DC coefficient of the preceding block
    prev_dc = 0

    for block in split_image(pix, im, block_size):
        # For each block, do:
        # Level adjustment
        # DCT
        # Quantization
        # 2D -> 1D
        # encode DC and AC coefficients

        block -= LEVEL_ADJUSTMENT
        block = DCT(block)
        block = quantization(block)
        array = zigzag(block)

        # encode DC and AC
        encoded = encode_coefficient(array, prev_dc)

        # output result
        result.extend(encoded)

    # add end of image bits
    result.extend("00")
    return result


def decompress(path_data, bit_array=None):
    # todo: store block x, y info
    if bit_array is None:
        array = load_bitarray(path_data)
    else:
        array = bit_array

    prev_dc = 0
    pos = 0

    # clamp value between 0, 255
    blocks = list()

    while pos < len(array):
        # check if end of image
        # because 00 represents huffman encoded size 0
        if array[pos:pos + 2] == bitarray("00"):
            break

        pos, coefficients = decode_coefficient(array, pos, prev_dc)

        # store previous DC coe
        prev_dc = coefficients[0]

        block = reverse_zigzag(coefficients)
        block = reverse_quantization(block)
        block = iDCT(block)
        block += LEVEL_ADJUSTMENT

        blocks.append(block)

    # todo: restore image
    return blocks
