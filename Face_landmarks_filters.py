import cv2
import os
import math
import cvzone
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceMeshModule import FaceMeshDetector

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
FaceDetector=FaceMeshDetector(maxFaces=2)

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
        

        


    except Exception as e:
        print(e)


        
    cameraFeedImg_flipped,faces=FaceDetector.findFaceMesh(cameraFeedImg_flipped,draw=False)
    #print(faces)
    try:
        for face in faces:
            xloc=face[21][0]
            yloc=face[21][0]
            if(isImageSelected):
                image=cv2.resize(menuImg[menuChoice],(100,100))
                cameraFeedImg_flipped=cvzone.overlayPNG(cameraFeedImg_flipped,menuImg[menuChoice],[int(indexFingerTop[0]),int(indexFingerTop[1])])
            else:
                distance=math.dist(face[21],face[251])

                scale=0
                dx=0
                dy=0
                if (menuChoice == 0):
                    scale=90
                    dx=5
                    dy=40
                if (menuChoice == 1):
                    scale=85
                    dx=5
                    dy=80
                if (menuChoice == 2):
                    scale=55
                    dx=20
                    dy=80
                if (menuChoice == 3):
                    scale=70
                    dx=15
                    dy=10
                if (menuChoice == 4):
                    scale=80
                    dx=10
                    dy=30

                resizeFactor=distance/scale
                
                xloc=int(xloc-(resizeFactor*dx))
                yloc=int(yloc-(resizeFactor*dy))
                
                filterImg=cv2.resize(menuImg[menuChoice],(100,100))
                filterImg=cv2.resize(filterImg,(0,0),fx=resizeFactor,fy=resizeFactor)
                cameraFeedImg_flipped=cvzone.overlayPNG(cameraFeedImg_flipped,filterImg,[xloc,yloc])



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