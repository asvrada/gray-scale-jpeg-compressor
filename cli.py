from src.jpeg import jpeg

import argparse
import os


def parse():
    desc = """\
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
    parser.add_argument("-q", "--quality", type=str, help="[DEFAULT: low] Define quality of JPEG image. One of {low, medium, high}", choices=["low", "medium", "high"], metavar='quality', default="low")

    argv = parser.parse_args()

    do_compress = argv.do_compress
    do_decompress = argv.do_decompress
    input_files = argv.files
    size = argv.size
    quality = argv.quality

    if do_compress and do_decompress:
        parser.print_help()
        exit(0)

    # If both False, set Defaul behavior to compress
    if not do_compress and not do_decompress:
        do_compress = True

    return do_compress, do_decompress, input_files, size, quality


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
        c = jpeg.Compressor(file, block_size=size, quality=quality).run()
        c.write_to_file(tmp_file)


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
        out_file = ".".join(file.split(".")[:-1]) + "_d.bmp"

        # decompress with hw2
        d = jpeg.Decompressor(file).run()
        d.write_to_file(out_file)


if __name__ == '__main__':
    do_compress, do_decompress, input_files, size, quality = parse()

    if do_compress:
        compress_skip(input_files, size, quality)

    elif do_decompress:
        decompress_skip(input_files)
