import cv2
import numpy as np
import CONFIG
from CONFIG import mycolours
from CONFIG import mycolourvalues

vid = cv2.VideoCapture(0) 

vid.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 650)
  


mypoints=[]



def getcontours(img):
      
    contours,hierarcy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        
        if area>500:
           # cv2.drawContours(imgresult,cnt,-1,(255,0,0),3)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h=cv2.boundingRect(approx)
    
    return x+w//2,y
def findcolour(image,mycolours,mycolourvalues):
      imghsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
      count=0
      newpoints=[]
      erase_lower=np.array([CONFIG.erase_hmin,CONFIG.erase_satmin,CONFIG.erase_valmin])
      erase_upper=np.array([CONFIG.erase_hmax,CONFIG.erase_satmax,CONFIG.erase_valmax])
      erase_mask=cv2.inRange(imghsv,erase_lower,erase_upper)
      erase_x,erase_y=getcontours(erase_mask)
      
      for colour in mycolours:
        lower=np.array(colour[0:3])
        upper=np.array(colour[3:6])
        mask=cv2.inRange(imghsv,lower,upper)
        x,y=getcontours(mask)
        
        if erase_x!=0 and erase_y!=0:
              cv2.rectangle(imgresult,(erase_x,erase_y),(erase_x+30,erase_y+20),(255,255,255),cv2.FILLED)
              

        if x!=0 and y!=0:
              cv2.circle(imgresult,(x,y),10,mycolourvalues[count],cv2.FILLED)
              
              newpoints.append([x,y,count])
        count+=1
        #cv2.imshow("Mask",mask)
      return newpoints,erase_x,erase_y

def drwaOnCanvas(mypoints,mycolourvalues):
      for pt in mypoints:
            cv2.circle(imgresult,(pt[0],pt[1]),10,mycolourvalues[pt[2]],cv2.FILLED)
            
            

while(True): 
      ret, frame = vid.read() 
      
      imgresult=frame.copy()
      #imgresult.setTo(0,0,0)
      newpoints,erase_x,erase_y=findcolour(frame,mycolours,mycolourvalues)
      if len(newpoints)!=0:
            for newp in newpoints:
                  mypoints.append(newp)
      if erase_x!=0 and erase_y!=0:
        for pt in mypoints:
          if (erase_x<pt[0]<(erase_x+30) and erase_y<pt[1]<erase_y+20):
            mypoints.remove(pt)            
      if len(mypoints)!=0:
            
        drwaOnCanvas(mypoints,mycolourvalues)            
      cv2.imshow('result', imgresult) 
      if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
vid.release() 
cv2.destroyAllWindows()