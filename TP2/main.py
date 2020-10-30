import matplotlib.pyplot as plt
import numpy as np
import math
import pywt

def sousEchantillonnage(img_yuv):
    width = len(img_yuv)
    height = len(img_yuv[0])
    Y = [[0]*width]*height
    U = [[0]*(width/2)]*(height/2)
    V = [[0]*(width/2)]*(height/2)
    for column in range(width):
        if column%2 == 0:
            for row in range(height):
                pixel = img_yuv[column][row]
                Y[column][row] = pixel[0]
                if row % 2 == 0:
                    U[column/2][row/2] = pixel[1]
                    V[column/2][row/2] = pixel[2]
        else:   
            for row in range(height):
                pixel = img_yuv[column][row]
                Y[column][row] = pixel[0]
            
    print(Y.size())
    print(V.size())
    print(U.size())
    return Y, U, V

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

def convertImageToRGB(img_yuv):
    RGB = img_yuv
    width = len(img_yuv)
    height = len(img_yuv[0])
    for column in range(width):
        for row in range(height):
            pixel = img_yuv[column][row]
            G = np.clip(pixel[0] - (pixel[1] + pixel[2]) / 4, 0, 255)
            R = np.clip(pixel[2] + G, 0, 255)
            B = np.clip(pixel[1] + G, 0, 255)
            RGB[column][row] = [R, G, B]

    return RGB

def DWT(img_YUV):
    cAy, (cHy, cVy, cDy) = pywt.dwt2(img_YUV[:, :, 0], 'haar')
    cAu, (cHu, cVu, cDu) = pywt.dwt2(img_YUV[:, :, 1], 'haar')
    cAv, (cHv, cVv, cDv) = pywt.dwt2(img_YUV[:, :, 2], 'haar')

    A = np.zeros((len(cAy), len(cAy[0]), 3))
    H = np.zeros((len(cHy), len(cHy[0]), 3))
    V = np.zeros((len(cVy), len(cVy[0]), 3))
    D = np.zeros((len(cDy), len(cDy[0]), 3))

    A[:,:,0] = cAy
    A[:,:,1] = cAu
    A[:,:,2] = cAv
    H[:,:,0] = cHy
    H[:,:,1] = cHu
    H[:,:,2] = cHv
    V[:,:,0] = cVy
    V[:,:,1] = cVu
    V[:,:,2] = cVv
    D[:,:,0] = cDy
    D[:,:,1] = cDu
    D[:,:,2] = cDv

    return A, H, V, D

DWT_recursion_level = 3

img_original = plt.imread('dank_luigi.jpeg').astype('int')
fig, (im) = plt.subplots(DWT_recursion_level + 1, 4)

im[0][0].imshow(img_original)
im[0][0].set_title("Image originale RGB")

img_YUV = convertImageToYUV(img_original)
im[0][1].imshow(img_YUV)
im[0][1].set_title("Image YUV")

#sousEchantillonnage(img_YUV.copy())

img_RGB = convertImageToRGB(img_YUV.copy())
im[0][2].imshow(img_RGB)
im[0][2].set_title("Image RGB")

fig.delaxes(im[0][3])

A = img_YUV.copy()
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

##############################################################################################
# 1D array
##############################################################################################
A = A.astype(int)
oneDimensionalImage = []
width = len(A)
height = len(A[0])
for column in range(width):
    for row in range(height):
        for color in range(3):
            oneDimensionalImage.append(A[column][row][color])
            
print(oneDimensionalImage)

##############################################################################################
#  LZW
##############################################################################################
dictsymb =[oneDimensionalImage[0]]
dictbin = ["{:b}".format(0)]
nbsymboles = 1
for i in range(1,len(oneDimensionalImage)):
    if oneDimensionalImage[i] not in dictsymb:
        dictsymb += [oneDimensionalImage[i]]
        dictbin += ["{:b}".format(nbsymboles)] 
        nbsymboles +=1
        
longueurOriginale = np.ceil(np.log2(nbsymboles))*len(oneDimensionalImage)    

for i in range(nbsymboles):
    dictbin[i] = "{:b}".format(i).zfill(int(np.ceil(np.log2(nbsymboles))))
        
dictsymb.sort()
dictionnaire = np.transpose([dictsymb,dictbin])
print(dictionnaire) 

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
