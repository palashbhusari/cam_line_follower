# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

rightpx_X=170
leftpx_Y=150
five=5

        


        
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))

time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        # cvrt to gray scale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #blur image to reduce noice
        blur = cv2.GaussianBlur(gray,(3,3),0)

        #drwa a ref line
        blur = cv2.line(blur,(160,0),(160,240),(0,255,0),1)
        #circlr# blur = cv2.circle(blur,(170,10),5,(0,0,255),1)
        blur = cv2.rectangle(blur,(rightpx_X,0),(rightpx_X+five,4),(0,0,255),1) #rigth1
        blur = cv2.rectangle(blur,(leftpx_Y-five,0),(leftpx_Y,4),(0,0,255),1) #left1

        blur = cv2.rectangle(blur,(191,0),(210,4),(0,0,255),1) #rigth2
        blur = cv2.rectangle(blur,(110,0),(130,4),(0,0,255),1) #left2
        #thresholding
        ret,thresh = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)
       

        rpx1 =blur[0:5,rightpx_X:rightpx_X+five]
        lpx1 =blur[0:5,leftpx_Y-five:leftpx_Y]
        r1=rpx1.mean()
        l1=lpx1.mean()
        
        print l1 ,'     ', r1
        if r1>90:
                print 'moveleft'
        if l1>90:
                print 'move right'
        # show the frame
        #cv2.imshow("normal", image)
        cv2.imshow("gray",blur)
        cv2.imshow("thresh",rpx1)
        
        key = cv2.waitKey(1) & 0xFF
 
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break
