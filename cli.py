from jpegcompressor import main as jpeg
from Compressor.compressor import Compressor

import argparse
import os


def compress_with_hw1(file):
    c = Compressor()
    c.compress_to_file(file, file + ".S")
    return file + ".S"


def decompress_with_hw1(file):
    c = Compressor()
    c.decompress_to_file(file, file[:-2])
    return file[:-2]


desc = """
Gray-scale only JPEG [De]Compressor by Zijie Wu
This program will [de]compress IN PLACE

Example usage:
    For compression: [DEFAULT]
        python cli.py -c image1.bmp image2.bmp ...
    For decompression: 
        python cli.py -d image1.cjpg image2.cjpg ...
"""

parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("-c", "--compress", dest="do_compress", help="[DEFAULT] Compress input file.", action="store_true")
parser.add_argument("-d", "--decompress", dest="do_decompress", help="Decompress input file.", action="store_true")
parser.add_argument("files", help="Path to gray-scale, bmp format images", nargs="+")
parser.add_argument("-s", "--size", type=int, help="[DEFAULT: 8] Define size of block, 8 or 16.", choices=[8, 16], metavar='size', default=8)

argv = parser.parse_args()

do_compress = argv.do_compress
do_decompress = argv.do_decompress
input_files = argv.files
size = argv.size

if do_compress and do_decompress:
    parser.print_help()
    exit(0)

# If both False, set Defaul behavior to compress
if not do_compress and not do_decompress:
    do_compress = True

if do_compress:
    print(">>> Compressing...")

    for file in input_files:
        print(">>> {}".format(file))

        # check file name
        if file[-3:] != "bmp":
            print("!!! Can't compress file: '{}', not bmp format!".format(file))
            continue

        # process file name
        out_file = ".".join(file.split(".")[:-1]) + ".cjpg"

        # compress with hw2
        jpeg.compress_to_file(file, out_file, size)

        # compress with hw1
        compress_with_hw1(out_file)

        # remove intermediate cjpg
        os.remove(out_file)

elif do_decompress:
    print(">>> Decompressing...")
    for file in input_files:
        print(">>> {}".format(file))

        # check file name
        if file[-6:] != "cjpg.S":
            print("Can't decompress file: {}, not .cjpg.S format!".format(file))
            continue

        # decompress with hw1
        cfile = decompress_with_hw1(file)

        # process file name
        # example file name: path/image.cjpg -> path/image
        out_file = ".".join(cfile.split(".")[:-1]) + "_d.bmp"

        # decompress with hw2
        jpeg.decompress_to_file(cfile, out_file)

        # remove intermediate cjpg
        os.remove(cfile)
