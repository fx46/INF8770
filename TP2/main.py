import matplotlib.pyplot as plt
import numpy as np

def convertImageToYUV(img_rgb):
    YUV = img_rgb
    width = len(img_rgb)
    height = len(img_rgb[0])
    for column in range(width):
        for row in range(height):
            pixel = img_rgb[column][row]
            YUV[column][row] = [
                (pixel[0] + 2 * pixel[1] + pixel[2]) / 4, 
                pixel[2] - pixel[1], 
                pixel[0] - pixel[2]
            ]

    return YUV

img_original = plt.imread('dank_luigi.jpeg').astype('int')

fig, (im1, im2) = plt.subplots(1,2)

im1.imshow(img_original)
im1.set_title("Image originale RGB")

img_YUV = convertImageToYUV(img_original)
im2.imshow(img_YUV)
im2.set_title("Image YUV")

plt.show()