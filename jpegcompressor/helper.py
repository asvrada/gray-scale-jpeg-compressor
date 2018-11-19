import numpy as np
from PIL import Image
import math

JPEG_QUANTIZATION_TABLE_8 = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                      [12, 12, 14, 19, 26, 58, 60, 55],
                                      [14, 13, 16, 24, 40, 57, 69, 56],
                                      [14, 17, 22, 29, 51, 87, 80, 62],
                                      [18, 22, 37, 56, 68, 109, 103, 77],
                                      [24, 35, 55, 64, 81, 104, 113, 92],
                                      [49, 64, 78, 87, 103, 121, 120, 101],
                                      [72, 92, 95, 98, 112, 100, 103, 99]])


def zigzag(block):
    """
    Flattern 2D matrix to 1D array, in a zigzag manner
    """
    array = list()

    pass


def get_dct_matrix(N):
    D = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i == 0:
                tmp = math.sqrt(1 / N)
            else:
                tmp = math.sqrt(2 / N)

            D[i][j] = tmp * math.cos(math.pi * (2 * j + 1) * i / (2 * N))

    return D


def DCT(block):
    """
    DCT on a copy of block
    """
    D = get_dct_matrix(block.shape[0])

    # D * A * D'
    return np.matmul(np.matmul(D, block), D.transpose())


def iDCT(block):
    """
    Inverse DCT
    """
    D = get_dct_matrix(block.shape[0])

    # D' * A * D
    return np.matmul(np.matmul(D.transpose(), block), D)


def quantization(block):
    """
    Quantize on a copy of block
    """
    if block.shape[0] == 8:
        return np.round(block / JPEG_QUANTIZATION_TABLE_8)

    table_16 = np.zeros((16, 16))
    for i in range(8):
        for j in range(8):
            table_16[2 * i][2 * j] = JPEG_QUANTIZATION_TABLE_8[i][j]
            table_16[2 * i + 1][2 * j] = JPEG_QUANTIZATION_TABLE_8[i][j]
            table_16[2 * i][2 * j + 1] = JPEG_QUANTIZATION_TABLE_8[i][j]
            table_16[2 * i + 1][2 * j + 1] = JPEG_QUANTIZATION_TABLE_8[i][j]

    return np.round(block / table_16)


def reverse_quantization(block):
    """
    Reverse quantize on a copy of block
    """
    if block.shape[0] == 8:
        return np.round(block * JPEG_QUANTIZATION_TABLE_8)

    table_16 = np.zeros((16, 16))
    for i in range(8):
        for j in range(8):
            table_16[2 * i][2 * j] = JPEG_QUANTIZATION_TABLE_8[i][j]
            table_16[2 * i + 1][2 * j] = JPEG_QUANTIZATION_TABLE_8[i][j]
            table_16[2 * i][2 * j + 1] = JPEG_QUANTIZATION_TABLE_8[i][j]
            table_16[2 * i + 1][2 * j + 1] = JPEG_QUANTIZATION_TABLE_8[i][j]

    return np.round(block * table_16)


def load_image(path_image):
    im = Image.open(path_image)
    pix = im.load()
    return pix, im


def split_image(pix, im, block_size=8):
    """
    A generator that split a image into blocks and return one block at a time
    :param pix: the pix object
    :param im: the im object
    :param block_size: the size of block, could be 8 or 16
    :type block_size: int
    :return: one block of a image
    :rtype: numpy.darray
    """
    height, width = im.size

    num_block_x = math.ceil(height / block_size)
    num_block_y = math.ceil(width / block_size)

    for x in range(num_block_x):
        for y in range(num_block_y):
            block = np.zeros((block_size, block_size))

            # construct block
            for i in range(block_size):
                for j in range(block_size):
                    # the index of pixel for the image
                    img_i, img_j = i + block_size * x, j + block_size * y

                    # skip out of bound
                    if img_i >= height or img_j >= width:
                        continue

                    # assign color
                    block[i][j] = pix[img_i, img_j]

            # yield one block
            yield block
