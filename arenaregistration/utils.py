import os
import matplotlib.image as mpimg
import cv2


def load_image(filename):
    if not os.path.isfile(filename):
        raise FileExistsError(f'File {filename} does not exist, cant load image')
    img = cv2.imread(filename)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)