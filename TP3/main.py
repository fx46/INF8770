import cv2

vidcap = cv2.VideoCapture('data/video/v01.mp4')
fps = vidcap.get(cv2.CAP_PROP_FPS)

img = cv2.imread('data/jpeg/i001.jpeg') 
average_img = img.mean(axis=0).mean(axis=0)

allTimeLow = 999999
frameNum = 0

while True:
    frameNum = frameNum + 1
    success, frame = vidcap.read()

    if not success:
        print("done!")
        break

    result = cv2.subtract(img,frame)
    average_result = result.mean(axis=0).mean(axis=0)

    brightness = sum(average_result)

    if brightness < allTimeLow:
        print("new low: " + str(brightness) + ", at frame: " + str(frameNum) + ", at second: " + str(frameNum / fps))
        allTimeLow = brightness