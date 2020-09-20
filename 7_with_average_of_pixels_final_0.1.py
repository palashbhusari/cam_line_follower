# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

x=5
y=3
rightpx_X=170    # right starting pixel
leftpx_X=150   # left starting pixel
yaxix=190
inc=5    # incremental value of pixel
kr=0     # weighted value for right side
kl=0     # weighted value for left side
pixels=range(0,5)    # range of pixels to check toward right &left
threshold =100#value which decides black or white  <150 = black
op=0

######################## functions

def check_upper():
        global kr
        global kl
        global blur
        global rightpx_X
        global leftpx_X
        global threshold
        global op
        global x
        global y
        #print 'frame'
        inc=5
        vals=[0] # append the pixels value in this list if it is on black surface
        
        i=1
        x=5
        y=3
        for p in pixels:
                
                r1=blur[yaxix,rightpx_X+inc]  # right side pixel value
                l1=blur[yaxix,leftpx_X-inc]   # left side pixel valude

                #drarw a rectangle
                blur = cv2.rectangle(blur,(rightpx_X+inc,yaxix-5),(rightpx_X+(inc+5),yaxix),(0,0,255),1) #rigth1
                blur = cv2.rectangle(blur,(leftpx_X-(inc+5),yaxix-5),(leftpx_X-inc,yaxix),(0,0,255),1)
        
                # checking for black surface.the More less value of r1,l1  the more black surface
                if r1<threshold:
                        kr=(i*x)
                        vals.append(kr)  #add the value in empty list vals
                else:
                        kr=0
                        vals.append(kr)
                        
                if l1<threshold:
                        kl=(i*-y)
                        vals.append(kl) #add the value in empty list vals for left side
                        
                else:
                        kl=0
                        vals.append(kl)
                        
                inc=inc+30
                i=i+1
                x=x+10
                y=y+10
        #########################
        op=sum(vals)
          
        return






    
                
 ############################### main code #########################################       
        
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 60
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


        check_upper() 
        print op

        #drwa a ref line
        blur = cv2.line(blur,(160,0),(160,240),(0,255,0),1)

        
        #thresholding
        #ret,thresh = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)
       
        
        # show the frame
        #cv2.imshow("normal", image)
        cv2.imshow("gray",blur)
        #cv2.imshow("thresh",rpx1)
        
        key = cv2.waitKey(1) & 0xFF
 
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break
