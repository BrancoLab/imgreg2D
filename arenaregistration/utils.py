import os
import matplotlib.image as mpimg


def load_image(filename):
    if not os.path.isfile(filename):
        raise FileExistsError(f'File {filename} does not exist, cant load image')
    return mpimg.imread(filename)