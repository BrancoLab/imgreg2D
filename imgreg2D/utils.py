import os
import numpy as np
import cv2


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