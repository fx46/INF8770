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

def DWT(img_YUV):
    cAr, (cHr, cVr, cDr) = pywt.dwt2(img_YUV[:, :, 0], 'haar')
    cAg, (cHg, cVg, cDg) = pywt.dwt2(img_YUV[:, :, 1], 'haar')
    cAb, (cHb, cVb, cDb) = pywt.dwt2(img_YUV[:, :, 2], 'haar')

    A = np.zeros((len(cAr), len(cAr[0]), 3))
    H = np.zeros((len(cHr), len(cHr[0]), 3))
    V = np.zeros((len(cVr), len(cVr[0]), 3))
    D = np.zeros((len(cDr), len(cDr[0]), 3))

    A[:,:,0] = cAr
    A[:,:,1] = cAg
    A[:,:,2] = cAb
    H[:,:,0] = cHr
    H[:,:,1] = cHg
    H[:,:,2] = cHb
    V[:,:,0] = cVr
    V[:,:,1] = cVg
    V[:,:,2] = cVb
    D[:,:,0] = cDr
    D[:,:,1] = cDg
    D[:,:,2] = cDb

    im[0].imshow(A)

    return A, H, V, D


img_original = plt.imread('dank_luigi.jpeg').astype('int')
fig, (im) = plt.subplots(1,6)

im[0].imshow(img_original)
im[0].set_title("Image originale RGB")

img_YUV = convertImageToYUV(img_original)
im[1].imshow(img_YUV)
im[1].set_title("Image YUV")

A, H, V, D = DWT(img_YUV)

im[2].imshow(A)
im[2].set_title("Approximation Coeff")
im[3].imshow(H)
im[3].set_title("Horizontal")
im[4].imshow(V)
im[4].set_title("Vertical")
im[5].imshow(D)
im[5].set_title("Diagonal")

plt.show()