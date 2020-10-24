import cv2
import numpy as np 
import cv2
vid = cv2.VideoCapture(0) 

def empty(a):
    
    pass


cv2.namedWindow("trackbars")
cv2.resizeWindow("trackbars",640,240)
cv2.createTrackbar("Hue Min","trackbars",3,179,empty)
cv2.createTrackbar("Hue Max","trackbars",97,179,empty)
cv2.createTrackbar("Sat Min","trackbars",155,255,empty)
cv2.createTrackbar("Sat Max","trackbars",226,255,empty)
cv2.createTrackbar("Val Min","trackbars",0,255,empty)
cv2.createTrackbar("Val Max","trackbars",255,255,empty)


while(True):
    
    ret, frame = vid.read() 
    original_img=frame.copy()
    imghsv=cv2.cvtColor(original_img,cv2.COLOR_BGR2HSV)
    hmin=cv2.getTrackbarPos("Hue Min","trackbars")
    hmax=cv2.getTrackbarPos("Hue Max","trackbars")
    satmin=cv2.getTrackbarPos("Sat Min","trackbars")
    satmax=cv2.getTrackbarPos("Sat Max","trackbars")
    valmin=cv2.getTrackbarPos("Val Min","trackbars")
    valmax=cv2.getTrackbarPos("Val Max","trackbars")
    lower=np.array([hmin,satmin,valmin])
    upper=np.array([hmax,satmax,valmax])
    mask=cv2.inRange(imghsv,lower,upper)
    imgResult=cv2.bitwise_and(original_img,original_img,mask=mask)
    cv2.imshow("Original",original_img)
    cv2.imshow("Mask",mask)
    cv2.imshow("Final Image",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
