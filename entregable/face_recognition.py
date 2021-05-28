import cv2
import dlib
from timeit import default_timer as timer

 
def recognition():
    
    start = timer()

    detector=dlib.get_frontal_face_detector()
    
    cap=cv2.VideoCapture(0)
    
    while True:
        _, frame= cap.read()
        
        gray= cv2.cvtColor(src=frame,code=cv2.COLOR_BGR2GRAY)
        
        faces=detector(gray)
        
        if len(faces) > 0:
            return True
        

        if (timer() - start) > 3:
            return False
    
    cap.release()
    

