import argparse
import os

from src.hw1.compressor import Compressor

parser = argparse.ArgumentParser(description="Sliding Window Decompressor by Zijie Wu\nExample usage:\ncli_file_decompress book1.txt ...", formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("files", help="Files to compress or decompress", nargs="*")

argv = parser.parse_args()

input_files = argv.files

c = Compressor()

print("Unzipping", input_files)
for each in input_files:
    c.decompress_to_file(each, each[:-2])
    os.remove(each)
