from imgreg2D.register import register
from imgreg2D.points import get_fixed_points

reference = 'media/original.jpg'
registering = 'media/rotated.jpg'

warp_mtx = 'warp_mtx.npy'

# ----------------------------- Get fixed points ----------------------------- #
points = get_fixed_points(reference)


# --------------------------------- Register --------------------------------- #
register(reference, registering, fixed_points = points)

# 3.4.1.15 in setup
# TODO change number of point requirement
# TODO test