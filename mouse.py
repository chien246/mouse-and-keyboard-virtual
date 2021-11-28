import cv2 as cv
import numpy as np
from TrackingModule import HandTracking
from pynput import mouse, keyboard
from utils import KeyButton, get_name_key
from time import sleep

handTracking = HandTracking()

cap = cv.VideoCapture(0)
cap.set(3,1080)
cap.set(4,720)
mode = 'null'

mouses = mouse.Controller()
keyBoard = keyboard.Controller()

point1 = (70,70)
point2 = (454,286)

smooth = 10
preLocationX, preLocationY = 0,0
curLocationX, curLocationY = 0,0

buttonSize = 40
haflButtonSize = int(buttonSize/2)
marginButton = 10
nomalButtonColor = (36,36,36)
digitButtonColor = (70,70,70)
hoverButtonColor = (77,77,77)
clickButtonColor = (172,172,255)

listChar = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
            ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'],
            ['U', 'V', 'W', 'X', 'Y', 'Z', '', '', '', ''],
            ['.', ',', '?', ';', '!', ':', '+', '-', '*', '/'],
            ['@', '#', '$', '%', '^', '&', '(', ')', '{', '}']]

def drawSingleButton(img, button, color):
    cv.rectangle(img, button.posStart, button.posEnd, color, -1)
    cv.putText(img, button.char, (button.posStart[0] + 10, button.posStart[1] + 20), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv.LINE_AA)

def drawKeyBoard(img):
    listButton = []
    x,y = -buttonSize, 60

    imgNew = np.zeros_like(img, np.uint8)

    for i,row in enumerate(listChar):
        for j,char in enumerate(row):
            x = x + buttonSize + marginButton
            if(char != ''):
                color = digitButtonColor if (char >= '0' and char <= '9') else nomalButtonColor
                button = KeyButton((x,y), (x+buttonSize, y+buttonSize), char)
                listButton.append(button)
                drawSingleButton(imgNew, button, color)
        x = -buttonSize
        y = y + buttonSize + marginButton

    x = x + buttonSize + marginButton
    tabButton = KeyButton((x,y), (x + buttonSize * 2 - haflButtonSize + marginButton, y + buttonSize), 'Tab')
    listButton.append(tabButton)
    drawSingleButton(imgNew, tabButton, nomalButtonColor)
    x += (buttonSize + marginButton) * 2 - haflButtonSize
    capButton = KeyButton((x, y), (x + buttonSize * 2 - haflButtonSize + marginButton, y + buttonSize), 'Caps')
    listButton.append(capButton)
    drawSingleButton(imgNew, capButton, nomalButtonColor)
    x += (buttonSize + marginButton) * 2 - haflButtonSize
    spaceButton = KeyButton((x, y), (x + buttonSize * 4 - haflButtonSize + marginButton * 3, y + buttonSize), 'Space')
    listButton.append(spaceButton)
    drawSingleButton(imgNew, spaceButton, nomalButtonColor)
    x += (buttonSize + marginButton) * 4 - haflButtonSize
    enterButton = KeyButton((x, y), (x + buttonSize * 2 - haflButtonSize + marginButton, y + buttonSize), 'Enter')
    listButton.append(enterButton)
    drawSingleButton(imgNew, enterButton, nomalButtonColor)
    x += (buttonSize + marginButton) * 2 - haflButtonSize
    backspaceButton = KeyButton((x, y), (x + buttonSize * 2 - haflButtonSize + marginButton, y + buttonSize), 'Del')
    listButton.append(backspaceButton)
    drawSingleButton(imgNew, backspaceButton, nomalButtonColor)




    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    return out, listButton

def isClickMode(landmarks):
    check_ngon_giua = handTracking.isRaiseFinger(landmarks, 'GIUA')
    check_ngon_cai = handTracking.isRaiseFinger(landmarks, 'CAI')
    check_ngon_ut = handTracking.isRaiseFinger(landmarks, 'UT')

    if((check_ngon_giua == True)
            and (check_ngon_cai == False)
            and (check_ngon_ut == False)):
        return True

    return False

def isScrollMode(landmarks):
    check_ngon_giua = handTracking.isRaiseFinger(landmarks, 'GIUA')
    check_ngon_cai = handTracking.isRaiseFinger(landmarks, 'CAI')
    check_ngon_ut = handTracking.isRaiseFinger(landmarks, 'UT')
    check_ngon_nhan = handTracking.isRaiseFinger(landmarks, 'NHAN')

    if ((check_ngon_giua == True)
            and (check_ngon_ut == True)
            and (check_ngon_nhan == True)
            and (check_ngon_cai == False)):
        return True

    return False

def isMoveMode(landmarks):
    check_ngon_giua = handTracking.isRaiseFinger(landmarks, 'GIUA')
    check_ngon_cai = handTracking.isRaiseFinger(landmarks, 'CAI')
    check_ngon_ut = handTracking.isRaiseFinger(landmarks, 'UT')
    check_ngon_nhan = handTracking.isRaiseFinger(landmarks, 'NHAN')
    check_ngon_tro = handTracking.isRaiseFinger(landmarks, 'TRO')

    if((check_ngon_cai == True)
        and (check_ngon_tro == True)
        and (check_ngon_giua == True)
        and (check_ngon_nhan == True)
        and (check_ngon_ut == True)):
        return True

    return False

def isKeyBoardMode(landmarks):
    check_ngon_giua = handTracking.isRaiseFinger(landmarks, 'GIUA')
    check_ngon_cai = handTracking.isRaiseFinger(landmarks, 'CAI')
    check_ngon_ut = handTracking.isRaiseFinger(landmarks, 'UT')
    check_ngon_nhan = handTracking.isRaiseFinger(landmarks, 'NHAN')

    if ((check_ngon_cai == True)
            and (check_ngon_giua == True)
            and (check_ngon_nhan == False)
            and (check_ngon_ut == False)):
        return True

    return False

while True:
    _, frame = cap.read()

    h,w,c = frame.shape

    landmarks = handTracking.findLandMark(frame)

    if(landmarks != None):
        #Move mode
        if(isMoveMode(landmarks)):
            cv.putText(frame, "Move mouse", point1, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
            cv.rectangle(frame, point1, point2, (255, 255, 0), 2)
            clickPoint = ((landmarks[12].x * w), (landmarks[12].y * h))
            if (clickPoint >= point1 and clickPoint <= point2):
                curLocationX = (clickPoint[0] - point1[0])/384 * 1920
                curLocationY = (clickPoint[1] - point1[1])/216 * 1080

                mouseLocationX = preLocationX + (curLocationX - preLocationX) / smooth
                mouseLocationY = preLocationY + (curLocationY - preLocationY) / smooth

                preLocationX = mouseLocationX
                preLocationY = mouseLocationY

                mouses.position = (mouseLocationX, mouseLocationY)
        #Click mode
        elif(isClickMode(landmarks)):
            cv.putText(frame, "Mouse", point1, cv.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv.LINE_AA)
            cv.rectangle(frame, point1, point2, (255, 255, 0), 2)
            clickPoint = ((landmarks[12].x*w), (landmarks[12].y*h))
            if(clickPoint >= point1 and clickPoint <= point2):
                curLocationX = (clickPoint[0] - point1[0]) / 384 * 1920
                curLocationY = (clickPoint[1] - point1[1]) / 216 * 1080

                mouseLocationX = preLocationX + (curLocationX - preLocationX) / smooth
                mouseLocationY = preLocationY + (curLocationY - preLocationY) / smooth

                preLocationX = mouseLocationX
                preLocationY = mouseLocationY

                mouses.position = (mouseLocationX, mouseLocationY)

                if(handTracking.isRaiseFinger(landmarks, 'CHUOTTRAI') == False and handTracking.isRaiseFinger(landmarks, 'CHUOTPHAI') == True):
                    print('left mouse clicked')
                    mouses.click(mouse.Button.left, 1)
                    sleep(0.25)
                elif (handTracking.isRaiseFinger(landmarks, 'CHUOTPHAI') == False and handTracking.isRaiseFinger(landmarks,'CHUOTTRAI') == True):
                    print('right mouse clicked')
                    mouses.click(mouse.Button.right, 1)
                    sleep(0.25)

        #Scroll mode
        elif(isScrollMode(landmarks)):
            cv.putText(frame, "Scroll", point1, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
            if (handTracking.isRaiseFinger(landmarks, 'CUON') == False):
                print('mouse scroll down')
                mouses.scroll(0, -1)
                sleep(0.1)
            elif (handTracking.isRaiseFinger(landmarks, 'CUON') == True):
                print('mouse scroll up')
                mouses.scroll(0, 1)
                sleep(0.1)

        elif(isKeyBoardMode(landmarks)):
            cv.putText(frame, "Keyboard", (40,40), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
            frame, listButton = drawKeyBoard(frame)

            x,y = ((landmarks[12].x * w), (landmarks[12].y * h))
            button = None
            for bt in listButton:
                if (bt.posStart[0] < x < bt.posEnd[0] and bt.posStart[1] < y < bt.posEnd[1]):

                    cv.rectangle(frame, bt.posStart, bt.posEnd, hoverButtonColor, -1)
                    cv.putText(frame, bt.char, (bt.posStart[0] + 10, bt.posStart[1] + 20),
                               cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv.LINE_AA)
                    button = bt
                    break

            if button != None:
                if handTracking.isRaiseFinger(landmarks, 'CHUOTTRAI') == False:
                    key = button.char if len(button.char) == 1 else get_name_key(button.char)
                    keyBoard.press(key)
                    sleep(0.25)

    cv.imshow("tracking", frame)
    cv.waitKey(1)