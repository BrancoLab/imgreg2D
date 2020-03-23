from imgreg2D.register import register
from imgreg2D.points import get_fixed_points

reference = 'media/original.jpg'
registering = 'media/rotated.jpg'

warp_mtx = 'warp_mtx.npy'

# ----------------------------- Get fixed points ----------------------------- #
points = [[1014.245,   998.5227],
 [1054.6302, 1111.0245],
 [1605.6005, 1235.065 ],
 [1596.9465, 1529.3003],
 [1031.553,  1584.1089],
 [ 970.9751, 1696.6106]]

# points = get_fixed_points(reference)


# --------------------------------- Register --------------------------------- #
register(reference, registering, fixed_points = points)