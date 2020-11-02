import matplotlib.pyplot as plt
import numpy as np
import math
import pywt
import os

def sousEchantillonnage(img_yuv):
    y = img_yuv[:, :, 0]

    u = img_yuv[:, :, 1]
    u = np.delete(u, list(range(0, u.shape[0], 2)), axis=1) #delete every other line
    u = u[::2] #delete every other column

    v = img_yuv[:, :, 2]
    v = np.delete(v, list(range(0, v.shape[0], 2)), axis=1) #delete every other line
    v = v[::2] #delete every other column

    return y, u, v

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
                pixel[0] - pixel[1]
            ]

    return YUV

def convertImageToRGB(y, u, v):
    width = len(y)
    height = len(y[0])
    RGB = []
    for column in range(width):
        RGB.append([])
        for row in range(height):
            # u and v are read with //2 for column and //2 for rows because of the 4:2:0 format
            G = np.clip(y[column][row] - (u[column//2][row//2] + v[column//2][row//2]) / 4, 0, 255).astype(np.uint8)
            R = np.clip(v[column//2][row//2] + G, 0, 255).astype(np.uint8)
            B = np.clip(u[column//2][row//2] + G, 0, 255).astype(np.uint8)
            RGB[column].append([R, G, B])

    return RGB

def DWT(y, u, v):
    cAy, _ = pywt.dwt2(y, 'haar')
    cAu, _ = pywt.dwt2(u, 'haar')
    cAv, _ = pywt.dwt2(v, 'haar')

    return cAy, cAu, cAv

def iDWT(y, u, v):
    cAy = pywt.idwt2((y, (None, None, None)), 'haar')
    cAu = pywt.idwt2((u, (None, None, None)), 'haar')
    cAv = pywt.idwt2((v, (None, None, None)), 'haar')

    return cAy, cAu, cAv

##############################################################################################
# Load image
##############################################################################################
DWT_recursion_level = 3
image_path = 'dank_luigi.jpeg'

img_original = plt.imread(image_path).astype('int')
longueurOriginale = os.stat(image_path).st_size * 8

fig, (im) = plt.subplots(1, 3)

im[0].imshow(img_original)
im[0].set_title("Image originale RGB")

##############################################################################################
# RGB to YUV
##############################################################################################
img_YUV = convertImageToYUV(img_original)
im[1].imshow(img_YUV)
im[1].set_title("Image YUV")

y = img_YUV[:, :, 0]
u = img_YUV[:, :, 1]
v = img_YUV[:, :, 2]

##############################################################################################
# Sous echantillonnage
##############################################################################################
y, u, v = sousEchantillonnage(img_YUV.copy())

##############################################################################################
# DWT
##############################################################################################
for i in range(DWT_recursion_level):
    y, u, v = DWT(y, u, v)

##############################################################################################
# 1D array
##############################################################################################
oneDimensionalImage = []

y = y.astype(int)
u = u.astype(int)
v = v.astype(int)

for column in range(len(y)):
    for row in range(len(y[0])):
        oneDimensionalImage.append(y[column][row])
for column in range(len(u)):
    for row in range(len(u[0])):
        oneDimensionalImage.append(u[column][row])
for column in range(len(v)):
    for row in range(len(v[0])):
        oneDimensionalImage.append(v[column][row])

##############################################################################################
#  1D array to LZW source: https://github.com/gabilodeau/INF8770
##############################################################################################
dictsymb =[oneDimensionalImage[0]]
dictbin = ["{:b}".format(0)]
nbsymboles = 1
for i in range(1,len(oneDimensionalImage)):
    if oneDimensionalImage[i] not in dictsymb:
        dictsymb += [oneDimensionalImage[i]]
        dictbin += ["{:b}".format(nbsymboles)] 
        nbsymboles +=1

for i in range(nbsymboles):
    dictbin[i] = "{:b}".format(i).zfill(int(np.ceil(np.log2(nbsymboles))))
        
dictsymb.sort()
dictionnaire = np.transpose([dictsymb,dictbin])

i=0
MessageCode = []
longueur = 0
while i < len(oneDimensionalImage):
    precsouschaine = oneDimensionalImage[i] 
    souschaine = oneDimensionalImage[i] 
    
    while souschaine in dictsymb and i < len(oneDimensionalImage):
        i += 1
        precsouschaine = souschaine
        if i < len(oneDimensionalImage):
            souschaine += oneDimensionalImage[i]  

    codebinaire = [dictbin[dictsymb.index(precsouschaine)]]
    MessageCode += codebinaire
    longueur += len(codebinaire[0]) 
    if i < len(oneDimensionalImage):
        dictsymb += [souschaine]
        dictbin += ["{:b}".format(nbsymboles)] 
        nbsymboles +=1
    
    if np.ceil(np.log2(nbsymboles)) > len(MessageCode[-1]):
        for j in range(nbsymboles):
            dictbin[j] = "{:b}".format(j).zfill(int(np.ceil(np.log2(nbsymboles))))

##############################################################################################
#  Taux de compression
##############################################################################################
print("Taux de compression = {0}".format(1 - longueur / longueurOriginale))

##############################################################################################
# Inverse DWT
##############################################################################################
for i in range(DWT_recursion_level):
    y, u, v = iDWT(y, u, v)

##############################################################################################
#  YUV to RGB
##############################################################################################
img_RGB = convertImageToRGB(y, u, v)
im[2].imshow(img_RGB)
im[2].set_title("Image RGB DWT lvl: " + str(DWT_recursion_level) + "\nTaux compression: \n" + str(1 - longueur / longueurOriginale))

##############################################################################################
#  plt 
##############################################################################################
plt.show()
