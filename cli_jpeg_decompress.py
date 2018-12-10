from src.jpeg.jpeg import Decompressor as jc
from src.hw1.compressor import Compressor as cc

import argparse
import os


def parse():
    desc = """\
Gray-scale image JPEG DECOMPRESSOR by Zijie Wu
This program will decompress input file IN PLACE

Example usage:
    jpeg_decompress image1.cjpg.S image2.cjpg.S ...
"""

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--skip", dest="noskip", help="Skip lossless compression. If skip, this program will receive .cjpg format rather that .cjpg.S", action="store_true")
    parser.add_argument("files", help="Path to gray-scale, cjpg or cjpg.S format images", nargs="+")

    argv = parser.parse_args()

    skip = argv.noskip
    input_files = argv.files

    return skip, input_files


def decompress_with_hw1(file):
    c = cc()
    c.decompress_to_file(file, file[:-2])
    return file[:-2]


def decompress(input_files):
    print(">>> Decompressing...")
    for file in input_files:
        print(">>> {}".format(file))

        # check file name
        if file[-6:] != "cjpg.S":
            print("Can't decompress file: {}, not .cjpg.S format!".format(file))
            continue

        # decompress with hw1
        tmp_file = decompress_with_hw1(file)

        # process file name
        # example file name: path/image.cjpg -> path/image
        out_file = ".".join(tmp_file.split(".")[:-1]) + ".bmp"

        # decompress with hw2
        d = jc(tmp_file).run()
        d.write_to_file(out_file)

        # remove intermediate cjpg
        os.remove(tmp_file)

        # remove original file
        os.remove(file)


def decompress_skip(input_files):
    print(">>> Decompressing and skip lossless decompression...")
    for file in input_files:
        print(">>> {}".format(file))

        # check file name
        if file[-4:] != "cjpg":
            print("Can't decompress file: {}, not .cjpg format!".format(file))
            continue

        # process file name
        # example file name: path/image.cjpg -> path/image
        out_file = ".".join(file.split(".")[:-1]) + ".bmp"

        # decompress with hw2
        d = jc(file).run()
        d.write_to_file(out_file)

        # remove original file
        os.remove(file)


if __name__ == '__main__':
    skip, input_files = parse()

    if not skip:
        decompress(input_files)
    else:
        decompress_skip(input_files)
