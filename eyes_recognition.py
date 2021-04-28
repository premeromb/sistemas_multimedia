import cv2
import dlib
import numpy as np
from timeit import default_timer as timer

 
def detector():
    

    detector = dlib.get_frontal_face_detector()
    
    cap = cv2.VideoCapture(2)
    start = timer()
    while(True):
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)
        
        if len(rects) > 0:
            #print ("Detectado")
            return True

        if (timer() - start) > 3:
                return False
        
    cap.release()
    cv2.destroyAllWindows()

#print(detector())