import cv2
import os
import math
import cvzone
from cvzone.HandTrackingModule import HandDetector

path="filters"

pathList=os.listdir(path)
pathList.sort
# print(pathList)
menuImg=[]

for i in pathList:
    img=(cv2.imread(path+"/"+i,cv2.IMREAD_UNCHANGED))
    img=cv2.resize(img,(100,100))
    menuImg.append(img)

# print(menuImg)
menuCount=len(menuImg)
print(menuCount)

cap=cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)

menuChoice=-1
isImageSelected=False

while True:
    check,cameraFeedImg=cap.read()
    cameraFeedImg_flipped=cv2.flip(cameraFeedImg,1)
    wHeight,wWidth,wChannel= cameraFeedImg_flipped.shape
    # print(wHeight,wWidth,wChannel)

    x=0
    xIncrement=math.floor(wWidth/menuCount)
    # print(xIncrement)

    
    
    handsDetector=detector.findHands(cameraFeedImg_flipped,flipType=False)
    # print("handsDetector", handsDetector)
    hands=handsDetector[0]
    cameraFeedImg_flipped=handsDetector[1]
    try:
        if hands:
            hand1=hands[0]
            lmList=hand1['lmList']
            indexFingerTop=lmList[8]
            indexFingerBottom=lmList[6]

            if indexFingerTop[1]<xIncrement:
                i=0
                while(xIncrement*i<=wWidth):
                    if(indexFingerTop[0] < xIncrement*i):
                        menuChoice=i-1
                        isImageSelected=True
                        break
                    i=i+1

            if (indexFingerTop[1] > indexFingerBottom[1]): 
                isImageSelected=False

            print(isImageSelected)

        if(isImageSelected):
            image=cv2.resize(menuImg[menuChoice],(100,100))
            cameraFeedImg_flipped=cvzone.overlayPNG(cameraFeedImg_flipped,menuImg[menuChoice],[int(indexFingerTop[0]),int(indexFingerTop[1])])

    except Exception as e:
        print(e)

    try:
        for i in menuImg:
            margin=20
            image=cv2.resize(i,(xIncrement-margin,xIncrement-margin))
            cameraFeedImg_flipped=cvzone.overlayPNG(cameraFeedImg_flipped,image,[x,0])
            x=x+xIncrement

    except:
            print("out of bounds")

        # cv2.imshow("MyVideo", cameraFeedImg)
    cv2.imshow("MyVideo_flip", cameraFeedImg_flipped)

    if cv2.waitKey(1) == 32:
         break