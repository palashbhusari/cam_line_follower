# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

from gpiozero import Motor
motor1=Motor(19,26)



rightpx_X=190    # right starting pixel
leftpx_X=130     # left starting pixel
inc=5    # incremental value of pixel
kr=0     # weighted value for right side
kl=0     # weighted value for left side
pixels=range(0,5)    # range of pixels to check toward right &left
threshold =150  #value which decides black or white  <150 = black
xr=[0]    #list for appending pixel val
xl=[0]   

######################## functions

def check_upper():
        global kr
        global kl
        global blur
        
        #print 'frame'
        
        inc=5
        vals=[0] # append the pixels value in this list if it is on black surface
        op=0 # output assignment
        i=1 # multiplier for the weighted values of pixels
        for p in pixels:
                
                
                #rpx1 =blur[0:2,rightpx_X+inc:rightpx_X+(inc+5)]
                #lpx1 =blur[0:2,leftpx_X-(inc+5):leftpx_X-inc]
             
                r1=blur[4,rightpx_X+inc]  # right side pixel value
                l1=blur[4,leftpx_X-inc]   # left side pixel valude

                #drarw a rectangle
                blur = cv2.rectangle(blur,(rightpx_X+inc,0),(rightpx_X+(inc+5),4),(0,0,255),1) #rigth1
                blur = cv2.rectangle(blur,(leftpx_X-(inc+5),0),(leftpx_X-inc,4),(0,0,255),1)
        
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





            

#################################
#############################
 ############################           
        print op   #### YAHA PRINT KIYA TO VALUE BARABAR AATI 
        return op  ###FIR RETURN KARKE FUNCTION ASIGN KIYA USKE BAD NAI AATI
        ### ISKE BAD NICHE DEKHNA
    
############################
############################
############################






    
                
 ############################### main code #########################################       
        
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







################################################
##################  RETURN PROBLEM#########################
#########################################        
        check_upper() 

        output=check_upper() ## FUNCTION KO ASSIGN KIYA FIR JO RETURN VALUE RAHEGI WO OUTPUT ME JAYEGI
        print 'op = ', output ## PAR ZERO HI AARA HAMESHA

##################################################
###############################################
#####################################








        
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
