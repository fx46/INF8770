import matplotlib.pyplot as plt
import numpy as np
import pywt
import cv2

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

fig, (im) = plt.subplots(1,5)

im[0].imshow(img_original)
im[0].set_title("Image originale RGB")

img_YUV = convertImageToYUV(img_original)
im[1].imshow(img_YUV)
im[1].set_title("Image YUV")

cAr, (cHr, cVr, cDr) = pywt.dwt2(img_YUV[:, :, 0], 'haar')
cAg, (cHg, cVg, cDg) = pywt.dwt2(img_YUV[:, :, 1], 'haar')
cAb, (cHb, cVb, cDb) = pywt.dwt2(img_YUV[:, :, 2], 'haar')

H = np.zeros((178,237,3))
V = np.zeros((178,237,3))
D = np.zeros((178,237,3))

H[:,:,0] = cHr
H[:,:,1] = cHg
H[:,:,2] = cHb
V[:,:,0] = cVr
V[:,:,1] = cVg
V[:,:,2] = cVb
D[:,:,0] = cDr
D[:,:,1] = cDg
D[:,:,2] = cDb

im[2].imshow(H)
im[2].set_title("Horizontal")
im[3].imshow(V)
im[3].set_title("Vertical")
im[4].imshow(D)
im[4].set_title("Diagonal")


plt.show()