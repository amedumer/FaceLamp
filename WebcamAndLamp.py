import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
import time
import pyfirmata


board = pyfirmata.Arduino('COM4')
board.digital[8].write(1)

faceCascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_alt2.xml")
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(1)
anterior = 0

while True:

    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    if len(faces) != 0:
        lastSuccess = time.time()
        board.digital[8].write(0)

    try:
        if time.time() - lastSuccess > 5:
            board.digital[8].write(1)
    except:
        pass


    
    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()