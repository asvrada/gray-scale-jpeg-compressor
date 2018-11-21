import numpy as np
from bitarray import bitarray

# the huffman table for encoding the size of DC / AC coe
HUFFMAN_TABLE = {
    0: "00",
    1: "010",
    2: "011",
    3: "100",
    4: "101",
    5: "110",
    6: "1110",
    7: "11110",
    8: "111110",
    9: "1111110",
    10: "11111110",
    11: "111111110"
}

# convert into bitarray
HUFFMAN_TABLE = {v: bitarray(k) for v, k in HUFFMAN_TABLE.items()}

JPEG_QUANTIZATION_TABLE_8 = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                      [12, 12, 14, 19, 26, 58, 60, 55],
                                      [14, 13, 16, 24, 40, 57, 69, 56],
                                      [14, 17, 22, 29, 51, 87, 80, 62],
                                      [18, 22, 37, 56, 68, 109, 103, 77],
                                      [24, 35, 55, 64, 81, 104, 113, 92],
                                      [49, 64, 78, 87, 103, 121, 120, 101],
                                      [72, 92, 95, 98, 112, 100, 103, 99]])
