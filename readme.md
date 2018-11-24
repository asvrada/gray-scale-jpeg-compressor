# Gray-scale Image Compressor / Decompressor

> Author: Zijie Wu  
> Date: 11/13/2018  
> Link: [here](http://www.cs.brandeis.edu/%7Estorer/cs175/Assignments/ProjectJPEG.html)

**JPEG Luminence Quantization Matrix**

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
 
 # Design
 
 ## Compression
 
 We are dealing with grayscale images. So some steps are skipped.
 
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
 
 ## Decompress

Do above steps in reverse order.

# Performance

To experiment with your program on the test data, you will need to be able to compare the quality of the decompressed image as compared to the original using the PSNR measure. You should make your own program to do this.
