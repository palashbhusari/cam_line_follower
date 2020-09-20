# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

rightpx_X=190    #right starting pixel
leftpx_X=130     # left starting pixel
inc=5    #increment value of pixel
kr=0
kl=0     # weighted value
pixels=range(0,4)    #range of pixels to check toward right &left



########################

def check_upper():
        global kr
        global kl
        global blur
       
        #print 'frame'
       
        inc=5
        xr=[0]
        xl=[0]
        i=1
        for p in pixels:
                
                blur = cv2.rectangle(blur,(rightpx_X+inc,0),(rightpx_X+(inc+5),4),(0,0,255),1) #rigth1
                blur = cv2.rectangle(blur,(leftpx_X-(inc+5),0),(leftpx_X-inc,4),(0,0,255),1)
                rpx1 =blur[0:2,rightpx_X+inc:rightpx_X+(inc+5)]
                lpx1 =blur[0:2,leftpx_X-(inc+5):leftpx_X-inc]
                r1=rpx1.mean()
                l1=lpx1.mean()

                if r1<70:
                        kr=(i*inc)/5
                        xr.append(kr)
                if l1<70:
                        kl=(i*inc)/5
                        xl.append(kl)
                else:
                        kr=0
                        kl=0
                inc=inc+20
                i=i+1
                
                
        print int(l1),'   ', int(r1) ,'      ' ,max(xl),'   ',max(xr)
        
                
 ########################################################################       
        
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

       ## blur = cv2.rectangle(blur,(rightpx_X,0),(rightpx_X+inc,4),(0,0,255),1) #rigth1
        ## blur = cv2.rectangle(blur,(leftpx_X-inc,0),(leftpx_X,4),(0,0,255),1) #left1
        
        
       

        check_upper() 
        
        
        # show the frame
        #cv2.imshow("normal", image)
        cv2.imshow("gray",blur)
        
        
        key = cv2.waitKey(1) & 0xFF
 
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break
