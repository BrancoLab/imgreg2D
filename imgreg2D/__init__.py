import os

# --------------------------------- BASE DIR --------------------------------- #
# Get/make secret folder

# _user_dir = os.path.expanduser("~")
# if not os.path.isdir(_user_dir):
#     raise FileExistsError("Could not find user base folder. Platform: {}".format(sys.platform))
# BASE_DIR = os.path.join(_user_dir, ".imgreg2D")

# if not os.path.isdir(BASE_DIR):
#     os.mkdir(BASE_DIR)

# # Remove all cached files
# for f in os.listdir(BASE_DIR):
#     os.remove(os.path.join(BASE_DIR, f))


# IMG_CACHE_PATH = os.path.join(BASE_DIR, 'fixed_points_image.png')

# ---------------------------------- AFFINE ---------------------------------- #
N_POINTS = 6

# ------------------------------- VISUALIZATION ------------------------------ #
POINTS_SIZE = 35
EDGE_WIDTH = 2