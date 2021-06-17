
import cv2
import time


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0


names = ['none', 'id 1', 'id 2'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
#cam.set(3, 480) # set video widht
#cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
button_state1 = False

while True:

    ret, img =cam.read()
    img = cv2.flip(img, 1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.1,
        minNeighbors = 5,
        minSize = (30, 30),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        conf=round(100 - confidence)
        
        # Check if confidence is less them 100 ==> "0" is perfect match
        if button_state1==False:
            if ( conf > 45):
                id = names[id]
                confidence = "  {0}%".format(conf)
                
            else:
                id = "unknown"
                confidence = "  {0}%".format(conf)
                
                     
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(conf), (x+5,y+h-5), font, 1, (255,255,0), 1)

    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(1) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
