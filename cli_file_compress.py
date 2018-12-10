import argparse
import os

from src.hw1.compressor import Compressor

parser = argparse.ArgumentParser(description="Sliding Window Compressor by Zijie Wu\nExample usage:\ncli_file_compress book1.txt ...", formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("files", help="Files to compress or decompress", nargs="*")
parser.add_argument("--size", type=int, help="Assign number of bits to sliding window\n9: 4K, 13: 64K", choices=[9, 13], metavar='size', default=9)

argv = parser.parse_args()

input_files = argv.files
size = argv.size

c = Compressor(size)

print("Zipping")
for each in input_files:
    print(each)
    c.compress_to_file(each, each + ".S")
    # remove original file
    os.remove(each)
