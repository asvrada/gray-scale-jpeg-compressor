from jpegcompressor.config import *
from jpegcompressor.helper import *

import numpy as np


def test_constant():
    assert LEVEL_ADJUSTMENT == 128
    assert type(HUFFMAN_TABLE_ENCODE) is dict
    assert HUFFMAN_TABLE_DECODE_ROOT is None
    assert JPEG_QUANTIZATION_TABLE_8.shape == (8, 8)


def test_zigzag():
    mat = np.round(np.random.rand(8, 8) * 256)
    array = zigzag(mat)
    new_mat = reverse_zigzag(array)
    assert mat.shape == new_mat.shape
    assert np.all(mat == new_mat)


def test_one_complement_encoding():
    pass


if __name__ == '__main__':
    test_constant()
    test_zigzag()
