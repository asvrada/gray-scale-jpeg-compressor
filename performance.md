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

## 8x8 block size

| Test File       | JPEG Compression | custom | gzip | compress |
|-----------------|------------------|--------|------|----------|
| Kodak08gray.bmp | 1.4              | 1.39   | 1.61 | 1.49     |
| Kodak09gray.bmp | 2.4              | 2.42   | 2.89 | 2.65     |
| Kodak12gray.bmp | 2.3              | 2.31   | 2.77 | 2.60     |
| Kodak18gray.bmp | 1.7              | 1.71   | 2.02 | 1.92     |
| Kodak21gray.bmp | 1.9              | 1.90   | 2.27 | 2.10     |
| Kodak22gray.bmp | 1.9              | 1.88   | 2.24 | 2.13     |

## 16x16 block size

| Test File       | JPEG Compression | custom | gzip | compress |
|-----------------|------------------|--------|------|----------|
| Kodak08gray.bmp | 1.34             | 1.35   | 1.56 | 1.45     |
| Kodak09gray.bmp | 2.40             | 2.41   | 2.86 | 2.63     |
| Kodak12gray.bmp | 2.25             | 2.26   | 2.70 | 2.54     |
| Kodak18gray.bmp | 1.69             | 1.69   | 1.99 | 1.90     |
| Kodak21gray.bmp | 1.86             | 1.87   | 2.22 | 2.07     |
| Kodak22gray.bmp | 1.86             | 1.86   | 2.21 | 2.09     |

# PSNR High (~50)

## 8x8 block size

| Test File       | JPEG Compression | custom | gzip | compress |
|-----------------|------------------|--------|------|----------|
| Kodak08gray.bmp | 1.26             | 1.26   | 1.45 | 1.35     |
| Kodak09gray.bmp | 2.09             | 2.10   | 2.48 | 2.26     |
| Kodak12gray.bmp | 2.03             | 2.04   | 2.41 | 2.26     |
| Kodak18gray.bmp | 1.54             | 1.54   | 1.79 | 1.69     |
| Kodak21gray.bmp | 1.68             | 1.69   | 1.99 | 1.83     |
| Kodak22gray.bmp | 1.67             | 1.68   | 1.97 | 1.84     |

## 16x16 block size

| Test File       | JPEG Compression | custom | gzip | compress |
|-----------------|------------------|--------|------|----------|
| Kodak08gray.bmp | 1.22             | 1.22   | 1.41 | 1.31     |
| Kodak09gray.bmp | 2.08             | 2.09   | 2.46 | 2.24     |
| Kodak12gray.bmp | 1.99             | 2.00   | 2.35 | 2.22     |
| Kodak18gray.bmp | 1.52             | 1.52   | 1.77 | 1.67     |
| Kodak21gray.bmp | 1.65             | 1.66   | 1.95 | 1.80     |
| Kodak22gray.bmp | 1.66             | 1.66   | 1.95 | 1.83     |