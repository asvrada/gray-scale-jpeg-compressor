from src.jpeg.jpeg import Decompressor as jc

import argparse
import os
import sys


def parse():
    desc = """\
Gray-scale image JPEG DECOMPRESSOR by Zijie Wu
This program will decompress input file IN PLACE

Example usage:
    jpeg_decompress image1.cjpg image2.cjpg ...
"""

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("files", help="Path to cjpg format file", nargs="*", default=sys.stdin.buffer, type=argparse.FileType('rb'))

    argv = parser.parse_args()

    buffer = argv.files

    return buffer


def decompress(buffer):
    if type(buffer) is list:
        # files
        for reader in buffer:
            filename = reader.name

            # process file name
            # example file name: path/image.cjpg -> path/image
            output_file = ".".join(filename.split(".")[:-1]) + ".bmp"

            # decompress with hw2
            d = jc(reader).run()
            d.write_to_file(output_file)

            # remove original file
            os.remove(filename)
    else:
        # stdin
        c = jc(buffer).run()
        c.write_to_stdout()


if __name__ == '__main__':
    buffer = parse()

    decompress(buffer)
