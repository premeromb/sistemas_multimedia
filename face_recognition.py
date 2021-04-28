import cv2
import dlib
 
 
def recognition():
    
    detector=dlib.get_frontal_face_detector()
    
    cap=cv2.VideoCapture(2)
    
    while True:
        _, frame= cap.read()
        
        gray= cv2.cvtColor(src=frame,code=cv2.COLOR_BGR2GRAY)
        
        faces=detector(gray)
        
        if len(faces) > 0:
            return True
        
        if(cv2.waitKey(delay=1))== 10:
            break
    
    cap.release()
    