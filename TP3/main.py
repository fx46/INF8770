import cv2
import time
import math
import os
import matplotlib.pyplot as plt 

#start_time = time.time()
#
#img = cv2.imread('data/png/i003.png') 
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
#        nameAllTimeLow = filename
#
#print("done!")
#print("At video: " + nameAllTimeLow)
#print("--- %s seconds ---" % (time.time() - start_time))






numWantedCaptures = 5

vidNum = 0
while vidNum <= 50:
    vidNum = vidNum + 1
    vidcap = cv2.VideoCapture('data/video/v' + str(vidNum) + '.mp4')
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(length)

    numFramesBetweenCaptures = math.floor(length / numWantedCaptures)

    frameNum = 0


    while True:

        success, frame = vidcap.read()
        frameNum = frameNum + 1

        if success:
            if frameNum == 1 or frameNum == math.floor(length / 2) or frameNum == length - 1: 
                cv2.imwrite('C:/Users/Efix/Documents/GitHub/INF8770/TP3/data/video/frames/v' + str(vidNum) + '_' + str(frameNum) + '.jpeg', frame)
        else:
            break







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
#    result = cv2.subtract(img,frame)
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