# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

rightpx_X=190    # right starting pixel
leftpx_X=130     # left starting pixel
inc=5    # incremental value of pixel
kr=0     # weighted value for right side
kl=0     # weighted value for left side
pixels=range(0,5)    # range of pixels to check toward right &left
threshold =150  #value which decides black or white  <150 = black
op=0

######################## functions #####################

def check_upper():
        global kr
        global kl
        global blur
        global rightpx_X
        global leftpx_X
        global threshold
        global op
        
        #print 'frame'
        inc=5
        vals=[0] # append the pixels value in this list if it is on black surface
        
        i=1
        for p in pixels:
                r1=blur[4,rightpx_X+inc]  # right side pixel value
                l1=blur[4,leftpx_X-inc]   # left side pixel valude
                # checking for black surface.the More less value of r1,l1  the more black surface
                if r1<threshold:
                        kr=(i*2)
                        vals.append(kr)  #add the value in empty list vals
                if l1<threshold:
                        kl=(i*-2)
                        vals.append(kl) #add the value in empty list vals for left side
                        
                else:
                        kr=0
                        kl=0
                inc=inc+15
                i=i+1
        #########################
        if len(vals) >1:
            op=( sum(vals)/(len(vals)-1) )
           
        return




  
                
 ############################### main code #########################################       
        
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 90
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

        # check for the black line
        check_upper() 
        print op
        
        key = cv2.waitKey(1) & 0xFF
 
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break
