#cameratest code 
import sys 
import zmq 
import socket 
import time 
import cv2 
from imutils.video import VideoStream 
import imagezmq 

sender = imagezmq.ImageSender(connect_to='tcp://10.144.113.180:5555') 
rpi_name = socket.gethostname() 
capture = cv2.VideoCapture(4) 
time.sleep(2) 
while capture.isOpened(): 
ret, frame = capture.read() 
if ret == True: 
frame = cv2.flip(frame, 90) 
cv2.imshow('Frame', frame) 
cv2.waitKey(1000) 
sender.send_image(rpi_name, frame) 
break 

time.sleep(1) 
capture.release() 
cv2.destroyAllWindows() 
