import os
import numpy as np
import cv2

from imgreg2D import CACHE_IMG_PATH

def create_marked_ref_image(img, points):
    "Adds a circle and a number to mark where the fixed points are on the template image"

    # Opencv font stuff
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 1
    fontColor              = (255, 40, 40)
    lineType               = 2

    # Check image is in RGB
    if len(img.shape) == 2:
        cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # Get image shape
    img_h, img_w, _ = img.shape

    # Add markers to where points are
    for n, point in enumerate(points):
        # flip the points until they match the orientation of the image
        point = point[::-1]
        # point[0] = img_w - point[0]
        # point[1] = img_h - point[1]

        # Add text and circle
        cv2.putText(
            img,
            str(n), 
            (int(point[0]-20), int(point[1]-20)), # bottom left corner of the text
            font, 
            fontScale,
            fontColor,
            lineType)

        cv2.circle(img, tuple(point), 10, [255, 0, 0], -1)
    return img


def load_image(filename):
    if not os.path.isfile(filename):
        raise FileExistsError(f'File {filename} does not exist, cant load image')
    img = cv2.imread(filename)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def save_warp_matrix(mtx, fld, name):
    if not fld:
        fld = os.getcwd()

    if not os.path.isdir(fld):
        os.mkdir(fld)
    
    name = name.replace(".npy", '')
    savename = os.path.join(fld, name+'.npy')

    np.save(savename, mtx)

def load_warp_matrix(filename):
    if not os.path.isfile(filename):
        raise FileExistsError(f'File {filename} does not exist, cant load warp matrix')
    if not '.npy' in filename:
        raise ValueError("'.npy' not in the filename but we're trying to load a numpy array.\n"+
               f"File path passed was {filename}")
    return np.load(filename)