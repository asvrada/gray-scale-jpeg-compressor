from src.jpeg.jpeg import Compressor as jc
from src.hw1.compressor import Compressor as cc

import argparse
import os


def parse():
    desc = """\
Gray-scale image JPEG COMPRESSOR by Zijie Wu
This program will compress input file IN PLACE

Example usage:
    jpeg_compress image1.bmp image2.bmp ...
"""

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--skip", dest="noskip", help="Skip lossless compression. Output file will be .cjpg format instead of .cjpg.S", action="store_true")
    parser.add_argument("files", help="Path to gray-scale, bmp format images", nargs="+")
    parser.add_argument("-s", "--size", type=int, help="[DEFAULT: 8] Define size of block, 8 or 16.", choices=[8, 16], metavar='size', default=8)
    parser.add_argument("-q", "--quality", type=str, help="[DEFAULT: medium] Define quality of JPEG image. One of {low, medium, high}", choices=["low", "medium", "high"], metavar='quality', default="medium")

    argv = parser.parse_args()

    skip = argv.noskip
    input_files = argv.files
    size = argv.size
    quality = argv.quality

    return skip, input_files, size, quality


def compress_with_hw1(file):
    c = cc()
    c.compress_to_file(file, file + ".S")
    return file + ".S"


def compress(input_files, size, quality):
    print(">>> Compressing...")

    for file in input_files:
        print(">>> {}".format(file))

        # check file name
        if file[-3:] != "bmp":
            print("!!! Can't compress file: '{}', not bmp format!".format(file))
            continue

        # process file name
        tmp_file = ".".join(file.split(".")[:-1]) + ".cjpg"

        # compress with hw2
        c = jc(file, block_size=size, quality=quality).run()
        c.write_to_file(tmp_file)

        # compress with hw1
        compress_with_hw1(tmp_file)

        # remove intermediate cjpg
        os.remove(tmp_file)

        # remove original file
        os.remove(file)


def compress_skip(input_files, size, quality):
    print(">>> Compressing and skip the lossless compression...")

    for file in input_files:
        print(">>> {}".format(file))

        # check file name
        if file[-3:] != "bmp":
            print("!!! Can't compress file: '{}', not bmp format!".format(file))
            continue

        # process file name
        tmp_file = ".".join(file.split(".")[:-1]) + ".cjpg"

        # compress with hw2
        c = jc(file, block_size=size, quality=quality).run()
        c.write_to_file(tmp_file)

        # remove original file
        os.remove(file)


if __name__ == '__main__':
    skip, input_files, size, quality = parse()

    if not skip:
        compress(input_files, size, quality)
    else:
        compress_skip(input_files, size, quality)
