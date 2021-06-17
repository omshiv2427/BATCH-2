import time
import cv2
import datetime
import sys
import telepot
import datetime as dt
from subprocess import call
import subprocess
import os.path
import cv2
import datetime as dt
from subprocess import CalledProcessError


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0
gchat_id=1126258930

names = ['none', 'id1', 'id2'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
#cam.set(3, 240) # set video widht
#cam.set(4, 240) # set video height

# Define min window size to be recognized as a face
count=0

#https://t.me/Path_predict_bot
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print(command)
    
    if command == '/image':
       bot.sendMessage(chat_id,text="Taking Photos")
       
       ret, frame = cam.read()
       if ret==True:
            frame = cv2.flip(frame,1)
            cv2.imwrite('./photo.jpg', frame)
            cv2.imshow('camera',frame) 
       else:
            bot.sendMessage(chat_id,text="Captured Failed")
       
       #cv2.destroyAllWindows()
       bot.sendPhoto(chat_id=chat_id, photo=open('./photo.jpg', 'rb'))
      

    elif command =='/video':
        bot.sendMessage(chat_id,text="Camera is starts recording")
        time.sleep(.1)
        bot.sendMessage(chat_id,text="Hold on please for 10 sec ")
        print('Start recording..')
        capture_duration = 10 #change here for duration of capturing video
        
        dim=(640,480)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('video.mp4',fourcc, 20.0, (640,480))
        start_time = time.time()
        while( int(time.time() - start_time) < capture_duration ):
            ret, frame = cam.read()
            if ret==True:
                frame = cv2.flip(frame,1)
                resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
                out.write(resized)
                cv2.imshow('camera',frame)                
            else:
                bot.sendMessage(chat_id,text="Record Failed")
                break
            k = cv2.waitKey(1) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
        
        out.release()
        #cam.release()
        #cv2.destroyAllWindows()
        
        print('Stop recording..')
        bot.sendMessage(chat_id,text="Recoding Completed")
        time.sleep(.1)
        bot.sendMessage(chat_id,text="Uploading video please be patient")
        time.sleep(.1)
        bot.sendVideo(chat_id, video=open('./video.mp4', 'rb'))


        
    elif (command=='hi') or (command=='Hi') or (command=='Hello') or (command=='hello') or (command=='Hey') or (command=='hey'):
        bot.sendMessage(chat_id,text="Hello \n /help")
    elif (command=='bye') or (command=='Bye') or (command=='See you') or (command=='take care') or (command=='Hey') or (command=='hey'):
        bot.sendMessage(chat_id,text="Have a Good Day")
    elif (command=='/-h') or (command=='/help') or (command=='/info') :
        bot.sendMessage(chat_id,text="Hello You Can Proceed with these commands \n /video \n /image")

def sendvid():
        global gchat_id
        chat_id=gchat_id
        bot.sendMessage(chat_id,text="Surveillance system Tracked Something!!!")
        time.sleep(.1)
        bot.sendMessage(chat_id,text="Hold on please for 10 sec ")
        print('Start recording..')
        capture_duration = 10 #change here for duration of capturing video
        
        dim=(640,480)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('video.mp4',fourcc, 20.0, (640,480))
        start_time = time.time()
        while( int(time.time() - start_time) < capture_duration ):
            ret, frame = cam.read()
            if ret==True:
                frame = cv2.flip(frame,1)
                resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
                out.write(resized)
                cv2.imshow('camera',frame)                
            else:
                bot.sendMessage(chat_id,text="Record Failed")
                break
            k = cv2.waitKey(1) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
        
        out.release()

        
        print('Stop recording..')
        bot.sendMessage(chat_id,text="Recoding Completed")
        time.sleep(.1)
        bot.sendMessage(chat_id,text="Uploading video")
        time.sleep(.1)
        bot.sendVideo(chat_id, video=open('./video.mp4', 'rb'))



bot = telepot.Bot('1739222778:AAEKgqSiboEBp58GP6iaBQZDrrCDoJyUMDY')
bot.message_loop(handle)
print('Video based surveillance system and path prediction')
bot.sendMessage(234352074,text="surveillance system,is Active Now")
bot.sendMessage(gchat_id,text="surveillance system,is Active Now")


def getCam():
    global count,chat_id
    
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
        if(id==1 and conf >35):
            if(x<100 or x >250):

                 count+=1
                 if(count>10):
                     sendvid()
                     bot.sendMessage(gchat_id,text="Predicting path please wait")
                     time.sleep(2)
                     if(x<100):
                         bot.sendMessage(gchat_id,text="Predicted Path person Moving Left direction")
                         bot.sendPhoto(chat_id=gchat_id, photo=open('./1.png', 'rb'))
                         count=0
                     
                     elif(x>250):
                         bot.sendMessage(gchat_id,text="Predicted Path person Moving Right direction")
                         bot.sendPhoto(chat_id=gchat_id, photo=open('./2.png', 'rb'))
                         count=0
                     else:
                         count=0
                      
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(conf), (x+5,y+h-5), font, 1, (255,255,0), 1)

    cv2.line(img=img, pt1=(int(150), 0), pt2=(int(150), 640), color=(0, 255, 0), thickness=2, lineType=1, shift=0)
    cv2.line(img=img, pt1=(int(470), 0), pt2=(int(470), 640), color=(0, 255, 0), thickness=2, lineType=1, shift=0)

    cv2.imshow('camera',img)


while (True):
 
    getCam()

    k = cv2.waitKey(1) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
        
cam.release()
cv2.destroyAllWindows()
