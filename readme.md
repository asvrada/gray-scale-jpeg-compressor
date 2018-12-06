# Gray-scale Image Compressor / Decompressor

> Author: Zijie Wu  
> Date: 11/13/2018  
> Page Link: [here](http://www.cs.brandeis.edu/%7Estorer/cs175/Assignments/ProjectJPEG.html)  
> GitHub: [here](https://github.com/asvrada/jpeg)

A gray-scale image compressor, can only compress images in .bmp format.

# How to use

```bash
# First:
cd /path/to/this/repo/

# To print help
python cli.py -h

# To compress gray-scale bmp image
python cli.py -c image.bmp

# To decompress
python cli.py -d image.cjpg.S
```

# Design

## Huffman table

```python
# the huffman table for [de]encoding the size of DC / AC coefficients
HUFFMAN_TABLE_ENCODE = {
    0: "00",
    1: "010",
    2: "011",
    3: "100",
    4: "101",
    5: "110",
    6: "1110",
    7: "11110",
    8: "111110",
    9: "1111110",
    10: "11111110",
    11: "111111110"
}
```

## Quality Levels:

1. Low, PSNR ~30
2. Medium, PSNR ~40
3. High, PSNR ~50

### Low quality
The **JPEG Luminence Quantization Matrix** used on low quality setting.

(From Table K.1 of the JPEG standard.) 

```
 16  11  10  16  24  40  51  61  
 12  12  14  19  26  58  60  55  
 14  13  16  24  40  57  69  56  
 14  17  22  29  51  87  80  62  
 18  22  37  56  68 109 103  77  
 24  35  55  64  81 104 113  92 
 49  64  78  87 103 121 120 101
 72  92  95  98 112 100 103  99
```
 
### Medium and High quality

Other quality are derived from above table, divided by a constant Q

* Q with low quality: 1
* Q with medium quality: 10
* Q with high quality: 20


## Compression
 
We are dealing with grayscale images. So its easy.
 
First:  
Block splitting (with options: 8x8, 16x16, pad with zero)
 
Then for each block, do:
 
 1. Level adjustment (subtract 128 from each byte)
 3. DCT
 4. Quantization then round to nearest int
 5. 2D -> 1D (zigzag odd)
 5. Encode DCT coefficients
    1. For DC component: Differential encoding
    2. For AC components: run-length encoding, with (0, 0) indicates the end of a block
 6. Compress whats left with external programs
    1. Compress
    2. gzip
    3. Compressor from HW1
 
## Decompression
 
Do above steps in reverse order.


# Implementation Details

* Use numpy for most math operations on matrix.
* Use PIL for image reading/writing.
* Use bitarray to store results. They can be easily converted to bytes then store to file, as well as read from file as bytes then creat bitarray from them.
* Build own huffman decode tree for huffman decoding/encoding.

### File description: 

* jpeg.py: Main file, where the main logic of compression/decompression happens
* huffman.py: Involves huffman encoding/decoding
* helper.py: A collections of functions that do specific things
* config.py: Constants (like quantization table, huffman table) go there


