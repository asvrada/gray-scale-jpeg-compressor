from bitarray import bitarray

from .config import *


def huffman_encode_to_bitarray(num):
    """
    Huffman encode the size of amplitude into bitarray

    :param num: the number of bits to represent amplitude
    :type num: int
    :return: huffman encoding
    :rtype: bitarray
    """

    return HUFFMAN_TABLE_ENCODE[num]


def build_huffman_decode_tree():
    """
    Build huffman decode tree from the specified huffman encode table

    :return: the root of the decode tree
    :rtype: TreeNode
    """

    def helper(root, pattern, val):
        if not root:
            root = TreeNode()

        if len(pattern) == 0:
            # end of pattern
            root.val = val
            return root

        # if is True
        if pattern[0]:
            # goto left child
            root.left = helper(root.left, pattern[1:], val)
        else:
            root.right = helper(root.right, pattern[1:], val)

        return root

    root = None

    # if tree is not constructed, build one first
    for val, pattern in HUFFMAN_TABLE_ENCODE.items():
        root = helper(root, pattern, val)

    return root


def huffman_decode(array, pos):
    """
    Decode the array using the pre-defined huffman tree, return the updated pos

    :param array: dont modify this!
    :type array: bitarray
    :param pos: the position of current index
    :type pos: int
    :return: tuple (pos, val), where pos = new position of index and val = decoded value
    :rtype: (int, int)
    """
    global HUFFMAN_TABLE_DECODE_ROOT
    if HUFFMAN_TABLE_DECODE_ROOT is None:
        HUFFMAN_TABLE_DECODE_ROOT = build_huffman_decode_tree()

    def helper(root, _pos):
        if root.val is not None:
            return _pos, root.val

        # is True, goto left
        if array[_pos]:
            return helper(root.left, _pos + 1)
        else:
            return helper(root.right, _pos + 1)

    return helper(HUFFMAN_TABLE_DECODE_ROOT, pos)
