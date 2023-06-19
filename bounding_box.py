import cv2
import numpy as np

# red = [0, 0, 255]

def get_limit(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lowerLimit = hsvC[0][0][0] - 10, 100, 100
    upperLimit = hsvC[0][0][0] + 10, 255, 255

    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)

    return lowerLimit, upperLimit

def box(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Merah
    red_low = np.array([0, 100, 100])
    red_up = np.array([0, 255, 255])

    # red_low, red_up = get_limit(color=red)

    #Hijau
    green_low = np.array([50, 100, 100])
    green_up = np.array([70, 255, 255])

    #Biru
    blue_low = np.array([100, 100, 100])
    blue_up = np.array([120, 255, 255])

    #KuningS
    yellow_low = np.array([20, 100, 100])
    yellow_up = np.array([40, 255, 255])

    red_mask = cv2.inRange(imgHSV, red_low, red_up)
    green_mask = cv2.inRange(imgHSV, green_low, green_up)
    blue_mask = cv2.inRange(imgHSV, blue_low, blue_up)
    yellow_mask = cv2.inRange(imgHSV, yellow_low, yellow_up)    

    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Merah
    for cnt in contours:
        area = cv2.contourArea(cnt)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
   
        x, y, w, h = cv2.boundingRect(approx)
        cv2.rectangle(img,(x,y), (x+w,y+h), (0,0,255), 3)
        cv2.putText(img, 'RED BALL', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0,0,255), 2)
        
    return img

vid = cv2.VideoCapture('vidio_demo.webm')

while True:
    success, frame = vid.read()

    if not success:
        continue

    bonding_box = box(frame)

    cv2.imshow('video', bonding_box)
    if cv2.waitKey(50) & 0xFF ==ord('q'):
        break
 