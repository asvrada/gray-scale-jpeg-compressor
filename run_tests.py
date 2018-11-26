from jpegcompressor.main import *

if __name__ == '__main__':
    test_image = "images/grayscale/Kodak09gray.bmp"
    output = "output.cjpg"

    compress_to_file(test_image, output, 8)

    decompress_to_file(output, "output.bmp")

    # test_image = "images/test.bmp"
    # array = compress_to_bitarray(test_image)
    #
    # result = decompress_bitarray(array)
    # result.save("output.bmp", "bmp")
