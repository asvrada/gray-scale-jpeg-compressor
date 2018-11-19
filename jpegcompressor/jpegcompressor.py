from .helper import *

LEVEL_ADJUSTMENT = 128


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
    :rtype: bytearray
    """
    pix, im = load_image(path_image)

    result = bytearray()

    for block in split_image(pix, im, block_size):
        # For each block, do:
        # Level adjustment
        # DCT
        # Quantization
        # 2D -> 1D

        # 1. Level adjustment
        block -= LEVEL_ADJUSTMENT

        # 2. DCT
        block = DCT(block)

        # 3. Quantization
        block = quantization(block)

        # 4. 2D -> 1D
        array = zigzag(block)

        # output result
        # todo: not right!
        result.extend(array)

    pass


if __name__ == '__main__':
    test_image = "../images/test.bmp"
    pix, im = load_image(test_image)
    ret = list(split_image(pix, im))

    print(len(ret))
