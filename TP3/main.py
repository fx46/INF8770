import cv2
import time

vidcap = cv2.VideoCapture('data/video/v01.mp4')
fps = vidcap.get(cv2.CAP_PROP_FPS)

img = cv2.imread('data/png/i001.png') 
average_img = img.mean(axis=0).mean(axis=0)

allTimeLow = 100
frameNum = 0

start_time = time.time()

while True:
    frameNum = frameNum + 1
    success, frame = vidcap.read()

    if not success:
        print("done!")
        print("did not find")
        print("--- %s seconds ---" % (time.time() - start_time))
        break

    result = cv2.subtract(img,frame)
    average_result = result.mean(axis=0).mean(axis=0)

    brightness = sum(average_result)

    if brightness < allTimeLow:
        
        allTimeLow = brightness

        if allTimeLow <= 1.0: # close enough to zero
            print("done!")
            print("At frame: " + str(frameNum) + ", at second: " + str(frameNum / fps))
            print("--- %s seconds ---" % (time.time() - start_time))
            break