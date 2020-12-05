import cv2
import time
import math
import os
import matplotlib.pyplot as plt 
import xlwt

###########################################################################
# Recherche d'une image parmis les frames pour obtenir la vidéo
###########################################################################
#
#start_time = time.time()
#
#img = cv2.imread('data/png/i001.png') 
#
#allTimeLow = 1000
#nameAllTimeLow = ''
#
#for filename in os.listdir('data/video/frames'):
#    frame = cv2.imread('data/video/frames/' + filename) 
#
#    if sum(img.mean(axis=0).mean(axis=0)) > sum(frame.mean(axis=0).mean(axis=0)):
#        result = cv2.subtract(img, frame)
#    else: 
#        result = cv2.subtract(frame, img)
#    average_result = result.mean(axis=0).mean(axis=0)
#
#    brightness = sum(average_result)
#
#    if brightness < allTimeLow:
#        allTimeLow = brightness
#        print(allTimeLow)
#        nameAllTimeLow = filename
#
#print("done!")
#print("At video: " + nameAllTimeLow)
#print("--- %s seconds ---" % (time.time() - start_time))
#
#
###########################################################################
# Méthode pour sauvegarder des frames d'une vidéo (pour faire comme BOB, 
# enlever numWantedCaptures et juste enregistrer chaque frames.
###########################################################################
#
#numWantedCaptures = 5
#
#vidNum = 0
#while vidNum <= 50:
#    vidNum = vidNum + 1
#    vidcap = cv2.VideoCapture('data/video/v' + str(vidNum) + '.mp4')
#    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
#
#    print(length)
#
#    numFramesBetweenCaptures = math.floor(length / numWantedCaptures)
#
#    frameNum = 0
#
#
#    while True:
#
#        success, frame = vidcap.read()
#        frameNum = frameNum + 1
#
#        if success:
#            if frameNum == 1 or frameNum == math.floor(length / 2) or frameNum == length - 1: 
#                cv2.imwrite('C:/Users/Efix/Documents/GitHub/INF8770/TP3/data/video/frames/v' + str(vidNum) + '_' + str(frameNum) + '.jpeg', frame)
#        else:
#            break



###########################################################################
# (question 3) Notre méthode d'enregistrer des frames si y'a beaucoup de 
# différence entre la dernière frame enregistrée.
###########################################################################
#
#vidNum = 0
#while vidNum <= 50:
#    vidNum = vidNum + 1
#    vidcap = cv2.VideoCapture('data/video/v' + str(vidNum) + '.mp4')
#    frameNum = 0
#    success, lastFrameCaptured = vidcap.read()
#    frameNum = frameNum + 1
#    cv2.imwrite('C:/Users/Efix/Documents/GitHub/INF8770/TP3/data/video/frames/v' + str(vidNum) + '_' + str(frameNum) + '.jpeg', lastFrameCaptured)
#
#    while True:
#        success, frame = vidcap.read()
#
#        if not success:
#            break
#
#        if sum(lastFrameCaptured.mean(axis=0).mean(axis=0)) > sum(frame.mean(axis=0).mean(axis=0)):
#            result = cv2.subtract(lastFrameCaptured, frame)
#        else: 
#            result = cv2.subtract(frame, lastFrameCaptured)
#        average_result = result.mean(axis=0).mean(axis=0)
#    
#        brightness = sum(average_result)
#    
#        if brightness >= 100: 
#            cv2.imwrite('C:/Users/Efix/Documents/GitHub/INF8770/TP3/data/video/frames/v' + str(vidNum) + '_' + str(frameNum) + '.jpeg', frame)
#            lastFrameCaptured = frame
#
#        frameNum = frameNum + 1



###########################################################################
# Une fois qu'on connait la vidéo d'ou provient l'image, on itère à travers
# chaque frame de la vidéo pour trouver le temps en secondes.
###########################################################################
#
#vidcap = cv2.VideoCapture('data/video/v01.mp4')
#fps = vidcap.get(cv2.CAP_PROP_FPS)
#
#img = cv2.imread('data/jpeg/i001.jpeg') 
#
#allTimeLow = 100
#frameNum = 0
#
#start_time = time.time()
#
#while True:
#    frameNum = frameNum + 1
#    success, frame = vidcap.read()
#
#    if not success:
#        print("done!")
#        print("did not find")
#        print("--- %s seconds ---" % (time.time() - start_time))
#        break
#
#    if sum(img.mean(axis=0).mean(axis=0)) > sum(frame.mean(axis=0).mean(axis=0)):
#        result = cv2.subtract(img, frame)
#    else: 
#        result = cv2.subtract(frame, img)
#    average_result = result.mean(axis=0).mean(axis=0)
#
#    brightness = sum(average_result)
#
#    if brightness < allTimeLow:
#        
#        allTimeLow = brightness
#
#        if allTimeLow <= 10.0: # close enough to zero, use 1.0 when using png
#            print("done!")
#            print("At frame: " + str(frameNum) + ", at second: " + str(frameNum / fps))
#            print(fps)
#            print("--- %s seconds ---" % (time.time() - start_time))
#            break


###########################################################################
# Alice
###########################################################################

book = xlwt.Workbook(encoding="utf-8")
sheet = book.add_sheet("sheet")

for imgNum in range(1, 201):
    print("finding image: " + str(imgNum))

    if imgNum < 10:
        img = cv2.imread('data/png/i00' + str(imgNum) + '.png') 
    elif imgNum < 100:
        img = cv2.imread('data/png/i0' + str(imgNum) + '.png') 
    else:
        img = cv2.imread('data/png/i' + str(imgNum) + '.png') 

    found = False
    allTimeLow = 10000
    start_time = time.time()

    for vidNum in range(1, 51):
        print("Analyzing video: " + str(vidNum))

        if vidNum < 10:
            vidcap = cv2.VideoCapture('data/video/v0' + str(vidNum) + '.mp4')
        else:
            vidcap = cv2.VideoCapture('data/video/v' + str(vidNum) + '.mp4')
            
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        frameNum = 0

        while True:
            frameNum = frameNum + 1
            success, frame = vidcap.read()

            if not success:
                #fin de video
                break

            if sum(img.mean(axis=0).mean(axis=0)) > sum(frame.mean(axis=0).mean(axis=0)):
                result = cv2.subtract(img, frame)
            else: 
                result = cv2.subtract(frame, img)
            average_result = result.mean(axis=0).mean(axis=0)
            brightness = sum(average_result)

            if brightness < allTimeLow:
                allTimeLow = brightness
                if allTimeLow <= 1.0: # close enough to zero, use bigger number (like 30) when using jpegs
                    sheet.write(imgNum, 0, "%s" % (time.time() - start_time))
                    sheet.write(imgNum, 1, "video: " + str(vidNum))
                    sheet.write(imgNum, 2, "minutage: " + str(frameNum / fps))
                    found = True
                    print("done!")
                    print("At frame: " + str(frameNum) + ", at second: " + str(frameNum / fps))
                    print("--- %s seconds ---" % (time.time() - start_time))
                    break

        if found:
            break

    if not found:
        print("not found!")
        print("--- %s seconds ---" % (time.time() - start_time))
        sheet.write(imgNum, 0, "%s" % (time.time() - start_time))
        sheet.write(imgNum, 1, "video: " + str(vidNum))

book.save("tempsAlice.xls")