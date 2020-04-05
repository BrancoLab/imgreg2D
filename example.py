from imgreg2D.register import register
from imgreg2D.points import get_fixed_points

reference = 'media/original.jpg'
registering = 'media/rotated.jpg'


# ----------------------------- Get fixed points ----------------------------- #
points = get_fixed_points(reference)


# --------------------------------- Register --------------------------------- #
warped_img, warp_mtx = register(reference, registering, fixed_points = points)