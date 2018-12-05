from jpegcompressor.jpeg import *

if __name__ == '__main__':
    input_file = "images/grayscale/Kodak08gray.bmp"
    output_compress = "output/test.cjpg"
    output_decompress = "output/decompress.bmp"

    c = Compressor(input_file, block_size=16).run()
    c.write_to_file(output_compress)

    d = Decompressor(output_compress).run()
    d.write_to_file(output_decompress)
