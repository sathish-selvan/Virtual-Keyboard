import cv2
from time import sleep
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, tuple(button.pos), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 68), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    return img

class Button():
    def __init__(self,pos,text,size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size

finalTest = ""
keyboard = Controller()
buttonList = []
keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ":"],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']]
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmlist, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmlist:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size

            if x < lmlist[8][0] < x+w and y<lmlist[8][1] <y+h:
                cv2.rectangle(img, tuple(button.pos), (x + w, y + h), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 68), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                l,_,_ = detector.findDistance(8,12,img)
                if l <30:
                    keyboard.press(button.text)
                    cv2.rectangle(img, tuple(button.pos), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 68), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                    finalTest += button.text
                    sleep(0.15)

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalTest, (60, 425), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

