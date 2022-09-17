import cv2
import mediapipe as mp

# to use a specific cam
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
#points on fingers
tipIds = [4, 8, 12, 16, 20]

while True:
     #to read the cam captuered
   success, img = cap.read()
   #To adjust the camera mode
    #img = cv2.flip(img , 0)
    
   # TO Convert image from bgr to rgb
   imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
   # to process image 
   results = hands.process(imgRGB)
   
   lmList = []
   
   #to check if there is hand or no
   if results.multi_hand_landmarks:
       for handLms in results.multi_hand_landmarks:
         for id, lm in enumerate(handLms.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
           # print(lmList)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            # to put circle around  specific point 
            if id == 8:
               cv2.circle(img, (cx, cy), 20, (0, 255, 0), cv2.FILLED)
             # to check if the finger open or close   
            if len(lmList) == 21: 
                fingers = []
                # for thumb finger to check it is open or close by cx 
                # 1 refers to cx & 0 refers to point 4 in thumb 
                if lmList[tipIds[0]][1] < lmList[tipIds[0] - 2][1]:
                   fingers.append(1)
                else:
                    fingers.append(0)
                
                #to check all fingers by cy - 2 
                for tip in range(1, 5):
                  if lmList[tipIds[tip]][2] < lmList[tipIds[tip] - 2][2]:
                     fingers.append(1)
                  else:
                     fingers.append(0)
            
               # print (fingers)    
                
                totalFingers = fingers.count(1)
                print(totalFingers)
                
                cv2.putText(img, f'{totalFingers}', (40, 80), cv2.FONT_HERSHEY_SIMPLEX,
               3, (0, 0, 255), 6)
                    #  # 8 & 6 refer to point in finger but 2 refers to cy 
                    # if lmList[8][2] < lmList[6] [2] : 
                    #     print('up')
                    # else :
                    #       print ('Down')
                                                   
       #print("Hand Detection")
    #nameofwindow & variable   
   cv2.imshow('Hand Tracker', img)
   #to break if user put skip
   if cv2.waitKey(5) & 0xff == 27:
      break    