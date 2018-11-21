from bitarray import bitarray
from .constants import HUFFMAN_TABLE


def huffman_encode_to_bitarray(num):
    """
    Huffman encode the size of amplitude into bitarray

    :param num: the number of bits to represent amplitude
    :type num: int
    :return: huffman encoding
    :rtype: bitarray
    """

    return HUFFMAN_TABLE[num]


def huffman_decode(array):
    # todo
    pass
