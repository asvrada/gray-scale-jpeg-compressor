import numpy as np
from PIL import Image
import math

from .huffman import *


def generate_quantization_table(q):
    A = np.zeros((8, 8))

    for i in range(1, 9):
        for j in range(1, 9):
            A[i - 1][j - 1] = 1 + q * (i + j - 1)

    return A


def encode_image_shape(size):
    """
    Encode image shape, 16 bits for each value

    :param size: a tuple contains (height, width)
    :type size: tuple
    :return: encoded height and width of the image
    :rtype: bitarray
    """
    height, width = size

    if height >= 2 ** 16 or width >= 2 ** 16:
        raise "Image too big, can't compress!"

    b_height = "{:016b}".format(height)
    b_width = "{:016b}".format(width)
    return bitarray(b_height + b_width)


def decode_image_shape(array, pos):
    """
    decode image shape from bitarray, starting from pos

    :param array: as usual, don't modify this array
    :type array: bitarray
    :param pos: starting index
    :type pos: int
    :return: a tuple of (pos, (height, weight))
    :rtype: (int, (int, int))
    """
    # we konw that each takes 16 bits
    height = int(array[pos:pos + 16].to01(), 2)
    width = int(array[pos + 16:pos + 32].to01(), 2)

    pos += 32

    return pos, (height, width)


def zigzag(matrix):
    """
    Flattern 2D matrix to 1D array, in a zigzag manner (odds)

    :return numpy array of int
    :rtype np.ndarray
    """
    r, c = 0, 0
    x, y = matrix.shape

    ret = np.zeros((x * y,), dtype=int)

    for i in range(x * y):
        ret[i] = matrix[r][c]

        if (r + c) % 2 == 0:
            if c == y - 1:
                r += 1
            elif r == 0:
                c += 1
            else:
                r -= 1
                c += 1
        else:
            if r == x - 1:
                c += 1
            elif c == 0:
                r += 1
            else:
                r += 1
                c -= 1

    return ret


def reverse_zigzag(array):
    r, c = 0, 0
    tmp_size = round(math.sqrt(len(array)))
    x, y = tmp_size, tmp_size

    ret = np.zeros((x * y,), dtype=int).reshape((x, y))

    for i in range(x * y):
        ret[r][c] = array[i]

        if (r + c) % 2 == 0:
            if c == y - 1:
                r += 1
            elif r == 0:
                c += 1
            else:
                r -= 1
                c += 1
        else:
            if r == x - 1:
                c += 1
            elif c == 0:
                r += 1
            else:
                r += 1
                c -= 1

    return ret


def convert_amp_to_bitarray(num):
    """
    Convert the amplitude into bitarray using 1's complement

    :param num: the number
    :type num: int
    :return: The 1's complement representation of the given number
    :rtype: bitarray
    """
    if num == 0:
        return bitarray()

    sign = True if num < 0 else False

    b_arr = bitarray("{:b}".format(abs(num)))

    # if negative, use complement
    if sign:
        one = len(b_arr) * bitarray('1')
        b_arr ^= one

    return b_arr


def revert_bitarray_to_amp(array):
    """

    :param array: bitarray
    :type array: bitarray
    :return:
    :rtype: int
    """
    if len(array) == 0:
        return 0

    sign = True if not array[0] else False

    # if negative, flip all the bits
    if sign:
        one = len(array) * bitarray('1')
        array ^= one

    num = int(array.to01(), 2)

    return num if not sign else -num


def encode_coefficient(array):
    """
    Encdoe DC and AC coefficient

    Encode into list of tuple (run, size, amplitude), while the first element is going to be (size, amplitude) since it's DC coe

    :param array: array of int
    :type array: np.ndarray
    :return: encoded DC and AC coefficient
    :rtype: bitarray
    """

    def convert_ac_to_bitarray(runlength, element):
        """
        Encode AC coe
        tuple: ((runlength, size), amplitude)
                where runlength is constrained to 4 bits, and size is huffman coded, amplitude is one's complement representation
            runlength: number of zero coe preceding this element
            size: number of bits requred to represent amplitude

        Special code:
            eob: (0, 0)
            zrl: (15, 0)

        :param runlength: time the element repeated
        :type runlength: int
        :param element: the AC amplitude
        :type element: int
        :return: encoded AC eoe
        :rtype: bitarray
        """
        # If there are more than 15 preceding zeros
        if runlength > max_runlength:
            return zrl + convert_ac_to_bitarray(runlength - max_runlength, element)

        b_runlength = bitarray("{:04b}".format(runlength))
        b_ac = convert_amp_to_bitarray(element)
        b_size = huffman_encode_to_bitarray(len(b_ac))

        return b_runlength + b_size + b_ac

    if len(array) not in [8 * 8, 16 * 16]:
        raise "Length of array to encode is not valid: got {}".format(len(array))

    # special code for encoding AC coe
    eob = bitarray("000000")
    zrl = bitarray("111100")
    max_runlength = 15

    result = bitarray()

    # First
    # encode DC first
    diff = array[0]

    # use one's complement representation
    b_diff = convert_amp_to_bitarray(diff)
    b_size = huffman_encode_to_bitarray(len(b_diff))

    # store results
    result.extend(b_size)
    result.extend(b_diff)

    # Second
    # encode AC
    count = 0
    for ac in array[1:]:
        # zero, increment count
        if ac == 0:
            count += 1
            continue

        # not zero, encode prev
        result.extend(convert_ac_to_bitarray(count, ac))
        # reset count
        count = 0

    # add end of block
    result.extend(eob)

    return result


def decode_coefficient(array, pos, prev_dc, block_size):
    """
    Decode the bitarray and construct the coefficients

    :param array:
    :type array: bitarray
    :param pos: starting index
    :type pos: int
    :param prev_dc:
    :type prev_dc: int
    :param block_size:
    :type block_size: int
    :return: the coefficients
    :rtype: (int, np.ndarray)
    """
    coefficients = list()

    # first, decode DC
    pos, size = huffman_decode(array, pos)

    diff = revert_bitarray_to_amp(array[pos:pos + size])
    pos += size

    dc = prev_dc + diff
    coefficients.append(dc)

    # Second: decode AC
    while True:
        # first 4 bits are runlength
        runlength = int(array[pos:pos + 4].to01(), 2)
        pos += 4

        # next huffman coded size
        pos, size = huffman_decode(array, pos)

        # check eob
        if runlength == 0 and size == 0:
            # fill 0
            num_zero = block_size ** 2 - len(coefficients)
            coefficients.extend([0] * num_zero)
            break

        # check zrl
        if runlength == 15 and size == 0:
            coefficients.extend([0] * 15)
            continue

        # then amplitude with size determined by huffman coded size
        ac = revert_bitarray_to_amp(array[pos:pos + size])
        pos += size

        coefficients.extend([0] * runlength)
        coefficients.append(ac)

    return pos, np.array(coefficients)


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
    return np.round(np.matmul(np.matmul(D.transpose(), block), D))


def quantization(block, table):
    """
    Quantize on a copy of block
    """
    return np.round(block / table)


def get_quantization_table(block_size, quality):
    mat = JPEG_QUANTIZATION_TABLE_8

    if block_size == 16:
        mat = np.zeros((16, 16))
        for i in range(8):
            for j in range(8):
                mat[2 * i][2 * j] = JPEG_QUANTIZATION_TABLE_8[i][j]
                mat[2 * i + 1][2 * j] = JPEG_QUANTIZATION_TABLE_8[i][j]
                mat[2 * i][2 * j + 1] = JPEG_QUANTIZATION_TABLE_8[i][j]
                mat[2 * i + 1][2 * j + 1] = JPEG_QUANTIZATION_TABLE_8[i][j]

    if quality == "low":
        return mat

    # set other quality
    scalar = {
        "medium": 8,
        "high": 10
    }

    return np.clip(np.round(mat / scalar[quality]), 1, 200)


def reverse_quantization(block, table):
    """
    Reverse quantize on a copy of block
    """
    return block * table


def load_image(path_image):
    im = Image.open(path_image)
    pix = im.load()
    return pix, im


def load_bitarray(path_data):
    """
    Load bitarray from file

    :param path_data:
    :type path_data: str
    :return: bitarray
    :rtype: bitarray
    """
    f = open(path_data, "rb")

    ret = bitarray()
    ret.fromfile(f)
    return ret


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
    width, height = im.size

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
                    # we reverse the index here because the coordinate for an image is different than for a 2D matrix
                    block[i][j] = pix[img_j, img_i]

            # yield one block
            yield block


def fill_image(draw, block, block_index, image_size):
    block_size = block.shape[0]
    x, y = block_index
    height, width = image_size

    for i in range(block_size):
        for j in range(block_size):
            img_i, img_j = i + block_size * x, j + block_size * y

            if img_i >= height or img_j >= width:
                continue

            # fill
            draw.point([(img_j, img_i)], fill=int(block[i][j]))
