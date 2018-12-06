from bitarray import bitarray
from PIL import Image, ImageDraw

from .helper import *
from .config import *


class Compressor:
    def __init__(self, image_path, block_size=8, quality="low"):
        """
        Create compressor object

        :param image_path: path to the image
        :type image_path: str
        :param block_size: size of each block before DCT, can be {8, 16}. Default to 8.
        :type block_size: int
        :param quality: Quality of compression, can be {"low", "medium" , "high"}. Default to "low".
        :type quality: str
        """
        # Create class variables
        self.__pix = None
        self.__im = None
        self.__result: bitarray = None
        self.__block_size = None
        self.__quality: str = None
        self.__quantization_table = None

        # Init class variables
        # check block size
        if block_size not in [8, 16]:
            raise Exception("block_size invalid")

        self.__block_size = block_size

        if quality not in ["low", "medium", "high"]:
            raise Exception("quality invalid")

        self.__quality = quality
        self.__quantization_table = get_quantization_table(self.__block_size, self.__quality)

        self.__pix, self.__im = load_image(image_path)
        self.__result = bitarray()

    def run(self):
        """
        Main entry. Start to compress the image

        :return: self
        :rtype: Compressor
        """
        self.__write_quality()
        self.__write_block_size()
        self.__write_image_shape()
        self.__write_blocks()
        return self

    def __write_blocks(self):
        prev_dc = 0
        for block in split_image(self.__pix, self.__im, self.__block_size):
            block -= LEVEL_ADJUSTMENT
            block = DCT(block)
            block = quantization(block, self.__quantization_table)
            array = zigzag(block)

            diff = array[0] - prev_dc
            prev_dc = array[0]
            array[0] = diff

            encoded = encode_coefficient(array)

            self.__result.extend(encoded)

        return self

    def __write_quality(self):
        """
        Store quality (2 bit) to the result
        00: low
        01: medium
        10: high

        :return: self
        :rtype: Compressor
        """
        quality_table = {
            "low": [False, False],
            "medium": [False, True],
            "high": [True, False]
        }

        self.__result.extend(quality_table[self.__quality])
        return self

    def __write_image_shape(self):
        """
        Store image shape
        Order: row, column

        :return: self
        :rtype: Compressor
        """
        width, height = self.__im.size

        # we store each dimension with 16 bits
        if height >= 2 ** 16 or width >= 2 ** 16:
            raise Exception("Image too big ( > 2^16), can't compress!")

        b_height = "{:016b}".format(height)
        b_width = "{:016b}".format(width)

        self.__result.extend(bitarray(b_height + b_width))
        return self

    def __write_block_size(self):
        """
        Store block size (1 bit)
        0: 8x8
        1: 16x16

        :return: self
        :rtype: Compressor
        """
        block_size_table = {
            8: [False],
            16: [True]
        }

        self.__result.extend(block_size_table[self.__block_size])
        return self

    def write_to_file(self, path_output_file):
        """
        Store the result to a file

        :param path_output_file: path to the output file
        :type path_output_file: str
        :return: self
        :rtype: Compressor
        """
        with open(path_output_file, "wb") as f:
            f.write(self.__result.tobytes())

        return self


class Decompressor:
    def __init__(self, image_path):
        """
        Create decompressor object

        :param image_path: path to image
        :type image_path: str
        """
        self.__array: bitarray = load_bitarray(image_path)
        self.__pos: int = 0

        self.__im = None
        self.__draw = None

        self.__quality: str = None
        self.__block_size: int = None
        self.__quantization_table: np.ndarray = None

        self.__image_height = None
        self.__image_width = None
        self.__num_block_row = None
        self.__num_block_col = None

    def run(self):
        self.__read_quality()
        self.__read_block_size()
        # we can get the quantization matrix from quality and block_size
        self.__generate_quantization_table()
        self.__read_image_shape()
        self.__read_blocks()

        return self

    def __read_quality(self):
        """
        Read quality from file

        :return: self
        :rtype: Decompressor
        """
        quality_table = {
            "00": "low",
            "01": "medium",
            "10": "high"
        }

        str_quality = self.__array[self.__pos:self.__pos + 2].to01()
        self.__pos += 2

        self.__quality = quality_table[str_quality]

        return self

    def __read_block_size(self):
        """
        Read block_size from file

        :return: self
        :rtype: Decompressor
        """
        block_size_table = {
            False: 8,
            True: 16
        }

        self.__block_size = block_size_table[self.__array[self.__pos]]
        self.__pos += 1

        return self

    def __generate_quantization_table(self):
        self.__quantization_table = get_quantization_table(self.__block_size, self.__quality)

    def __read_image_shape(self):
        self.__pos, (self.__image_height, self.__image_width) = decode_image_shape(self.__array, self.__pos)

        self.__im = Image.new("L", (self.__image_width, self.__image_height))
        self.__draw = ImageDraw.Draw(self.__im)

        self.__num_block_row = math.ceil(self.__image_height / self.__block_size)
        self.__num_block_col = math.ceil(self.__image_width / self.__block_size)

        return self

    def __read_blocks(self):
        prev_dc = 0

        for count in range(self.__num_block_row * self.__num_block_col):
            self.__pos, coefficients = decode_coefficient(self.__array, self.__pos, prev_dc, self.__block_size)

            prev_dc = coefficients[0]

            block = reverse_zigzag(coefficients)
            block = reverse_quantization(block, self.__quantization_table)
            block = iDCT(block)
            block += LEVEL_ADJUSTMENT

            block = np.clip(block, 0, 255)

            block_x = count // self.__num_block_col
            block_y = count % self.__num_block_col
            fill_image(self.__draw, block, (block_x, block_y), (self.__image_height, self.__image_width))

        return self

    def write_to_file(self, path_output_file):
        self.__im.save(path_output_file, "bmp")
        return self
