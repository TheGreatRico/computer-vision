import os
import numpy as np
import cv2
from pyzbar.pyzbar import decode


def show_image(img, fullscreen=False):
    """
    Helper function to render the image
    """
    if fullscreen:
        cv2.namedWindow('scanned_image', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('scanned_image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('scanned_image', img)
    cv2.waitKey()
    cv2.destroyWindow('scanned_image')


INPUT_DIR = 'data'

for i in os.listdir(INPUT_DIR):
    # loading the image through the open-cv library
    img = cv2.imread(os.path.join(INPUT_DIR, i))

    # decoding the image with the pyzbar's decode
    qr_decoded = decode(img)

    for qr in qr_decoded:
        # extracting information from the decoded image
        data = qr.data
        rectangle = qr.rect
        polygon = qr.polygon

        # printing interesting information
        print(f'Data in the QR code: {data} from the {i} picture')
        print(f'The rectangle position: {rectangle}')
        print(f'Coordinates of each corner of the polygon: {polygon[0]}')

        # adding boundary box around the QR code area
        cv2.rectangle(img, (rectangle.left, rectangle.top),
                      (rectangle.left + rectangle.width, rectangle.top + rectangle.height), (25, 200, 25), 3)

        # adding the outline around the QR code itself
        cv2.polylines(img, [np.array(polygon)], True, (126, 52, 255), 3)

        show_image(img, fullscreen=False)
