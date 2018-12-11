#!/usr/bin/env python

from src.jpeg import Compressor as jc

import argparse
import os
import sys


def parse():
    desc = """\
Gray-scale image JPEG COMPRESSOR by Zijie Wu
This program will compress input file IN PLACE

Example usage:
    jpeg_compress image1.bmp image2.bmp ...
"""

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", help="Path to gray-scale, bmp format images", nargs="*", default=sys.stdin.buffer, type=argparse.FileType('rb'))
    parser.add_argument("-s", "--size", type=int, help="[DEFAULT: 8] Define size of block, 8 or 16.", choices=[8, 16], metavar='size', default=8)
    parser.add_argument("-q", "--quality", type=str, help="[DEFAULT: medium] Define quality of JPEG image. One of {low, medium, high}", choices=["low", "medium", "high"], metavar='quality', default="medium")
    argv = parser.parse_args()

    buffered_reader = argv.files
    size = argv.size
    quality = argv.quality

    return buffered_reader, size, quality


def compress(buffered_reader, size, quality):
    if type(buffered_reader) is list:
        # List of files
        for reader in buffered_reader:
            filename = reader.name

            # generate new file name
            output_file = ".".join(filename.split(".")[:-1]) + ".cjpg"

            # compress
            c = jc(reader, block_size=size, quality=quality).run()
            c.write_to_file(output_file)

            # remove original file
            os.remove(filename)
    else:
        # read from stdin
        c = jc(buffered_reader, block_size=size, quality=quality).run()
        c.write_to_stdout()


if __name__ == '__main__':
    buffered_reader, size, quality = parse()

    compress(buffered_reader, size, quality)
