All test files are of the same size: **394,296** bytes.  
All size in bytes.  
All compression are represented as ratio, calculated by `original_size / compressed_size`.

# PSNR Low (~30)
## 8x8 block size

| Test File       | JPEG compression | custom lossless compressor | gzip | compress | PSNR    |
|-----------------|---------------|--------------------|------|----------|---------|
| Kodak08gray.bmp | 3.9              | 3.9                         | 4.7  | 4.3      | 30.1559 |
| Kodak09gray.bmp | 9.2              | 9.5                         | 11.6 | 10.2     | 35.5095 |
| Kodak12gray.bmp | 8.3              | 8.6                         | 10.6 | 9.5      | 35.3124 |
| Kodak18gray.bmp | 5.2              | 5.3                         | 6.5  | 6.1      | 31.7890 |
| Kodak21gray.bmp | 6.3              | 6.5                         | 8.0  | 7.3      | 32.3932 |
| Kodak22gray.bmp | 6.2              | 6.4                         | 7.9  | 7.3      | 33.2675 |

## 16x16 block size

| Test File       | JPEG compression | custom | gzip | compress | PSNR    |
|-----------------|------------------|--------|------|----------|---------|
| Kodak08gray.bmp | 3.7              | 3.8    | 4.5  | 4.2      | 30.1296 |
| Kodak09gray.bmp | 9.6              | 9.8    | 11.6 | 10.1     | 35.5900 |
| Kodak12gray.bmp | 8.4              | 8.6    | 10.3 | 9.2      | 35.3321 |
| Kodak18gray.bmp | 5.1              | 5.3    | 6.4  | 5.9      | 31.8113 |
| Kodak21gray.bmp | 6.3              | 6.4    | 7.8  | 7.1      | 32.4166 |
| Kodak22gray.bmp | 6.2              | 6.4    | 7.8  | 7.2      | 33.3218 |

# PSNR Medium (~40)