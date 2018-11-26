from jpegcompressor import main as jpeg

import argparse

desc = """
Gray-scale only JPEG [De]Compressor by Zijie Wu

Example usage:
    For compression:
        python cli.py -c image1.bmp image2.bmp ...
    For decompression: 
        python cli.py -d compressed.file1 compressed.file2 ...
"""

parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("-c", "--compress", dest="do_compress", help="[DEFAULT] Compress input file.", action="store_true")
parser.add_argument("-d", "--decompress", dest="do_decompress", help="Decompress input file.", action="store_true")
parser.add_argument("files", help="Files to compress or decompress", nargs="+")
parser.add_argument("-s", "--size", type=int, help="[DEFAULT: 8] Define size of block, 8 or 16.", choices=[8, 16], metavar='size', default=8)

argv = parser.parse_args()
do_compress = argv.do_compress
do_decompress = argv.do_decompress
input_files = argv.files
size = argv.size

if do_compress and do_decompress:
    parser.print_help()
    exit(0)

print(do_compress, do_decompress, input_files, size)
