import os

# --------------------------------- BASE DIR --------------------------------- #
# Get/make cache folder
_user_dir = os.path.expanduser("~")
if not os.path.isdir(_user_dir):
    raise FileExistsError("Could not find user base folder. Platform: {}".format(sys.platform))
BASE_DIR = os.path.join(_user_dir, ".imgreg2D")

if not os.path.isdir(BASE_DIR):
    os.mkdir(BASE_DIR)

CACHE_IMG_PATH = os.path.join(BASE_DIR, 'cache.png')

# ---------------------------------- AFFINE ---------------------------------- #
MIN_N_POINTS = 6 # Minimum number of points needed

# ------------------------------- VISUALIZATION ------------------------------ #
POINTS_SIZE = 35
EDGE_WIDTH = 2