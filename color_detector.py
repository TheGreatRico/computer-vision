import cv2
import numpy as np
from PIL import Image


def make_limits(color, interval):
    col = np.uint8([[color]])  # the BGR values which we want to convert to hsv

    # http://www.ece.northwestern.edu/local-apps/matlabhelp/toolbox/images/hsvcone.gif
    # convert BGR to hue - saturation - value color scheme
    hsv_col = cv2.cvtColor(col, cv2.COLOR_BGR2HSV) 
    # we will use hue to determine all colors of one 'family', like red or green
    # we could think of it as if we take the whole sector of the circle
    # https://ljplus.ru/img4/z/h/zhur74/05_Cvetovoy_krug_HSB.jpg
    hue = hsv_col[0][0][0]  # Get the hue value

    # Since hue has circular format, it wraps around itself on red color.
    # To be able to set correct interval for red we need to code the
    # conditions to calculate correct values
    if hue >= 165:  # Upper limit for divided red hue
        left_limit = np.array([hue - interval/2, 100, 100], dtype=np.uint8)
        right_limit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        left_limit = np.array([0, 100, 100], dtype=np.uint8)
        right_limit = np.array([hue + interval/2, 255, 255], dtype=np.uint8)
    else:
        left_limit = np.array([hue - interval/2, 100, 100], dtype=np.uint8)
        right_limit = np.array([hue + interval/2, 255, 255], dtype=np.uint8)

    return left_limit, right_limit


color = [0, 0, 255] # color we want to detect in BGR colorspace, currently detecting red
capture = cv2.VideoCapture(0) # Capture video from cam #0 (default if one cam is connected)
while True:
    _, frame = capture.read() # returns a tuple consisting of a Boolean value and
                              # the image data as a NumPy array. Bool indicates
                              # success of read operation.

    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Using cv2.cvtColor() method 
                                                       # Using cv2.COLOR_BGR2HSV color space 
                                                       # conversion code 


    left_limit, right_limit = make_limits(color=color, interval=20) # determine the limits of color
                                                                   # in set interval
    mask = cv2.inRange(hsv_image, left_limit, right_limit) # making masked image from current frame
                                                           # that only detects one color in a set range

    boundary_box_mask = Image.fromarray(mask) # to draw the rectangle around detected object we get
                                              # array of coordinates from mask using PIL library
    boundary_box = boundary_box_mask.getbbox() # now we simply save coordinates to a new variable

    if boundary_box is not None:
        x1, y1, x2, y2 = boundary_box # coordinates are the edges of the box that surrounds the mask
        cv2.rectangle(img=frame, pt1=(x1, y1), 
                      pt2=(x2, y2), color=(255, 255, 0), thickness=3) # now we draw the rectangle

    # labeling the windows
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_position = (250, 50)
    font_scale = 1
    font_color = (255, 255, 100)
    thickness = 2
    line_type = 1
    cv2.putText(frame,'Webcam', text_position, font, font_scale, font_color, thickness, line_type)
    cv2.putText(mask,'Mask', text_position, font, font_scale, font_color, thickness, line_type)

    cv2.imshow('webcam', frame) # draw a window with the actual frame with the box in it
    cv2.imshow('mask', mask) # draw masked frame to see what the program is detecting
    if cv2.waitKey(1) & 0xFF == ord('x'): # simple way to exit the program
        break

capture.release()
cv2.destroyAllWindows() # clean the memory after we're done