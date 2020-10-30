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

    return A, H, V, D

DWT_recursion_level = 3

img_original = plt.imread('dank_luigi.jpeg').astype('int')
fig, (im) = plt.subplots(4, DWT_recursion_level + 1)

im[0][0].imshow(img_original)
im[0][0].set_title("Image originale RGB")

img_YUV = convertImageToYUV(img_original)
im[0][1].imshow(img_YUV)
im[0][1].set_title("Image YUV")

fig.delaxes(im[0][2])
fig.delaxes(im[0][3])

A = img_YUV
for i in range(DWT_recursion_level):
    A, H, V, D = DWT(A)
    
    im[1 + i][0].imshow(A)
    im[1 + i][0].set_title("Approximation Coeff " + str(i + 1))
    im[1 + i][1].imshow(H)
    im[1 + i][1].set_title("Horizontal " + str(i + 1))
    im[1 + i][2].imshow(V)
    im[1 + i][2].set_title("Vertical " + str(i + 1))
    im[1 + i][3].imshow(D)
    im[1 + i][3].set_title("Diagonal " + str(i + 1))

plt.show()