from imgreg2D.register import register
from imgreg2D.points import get_fixed_points

reference = 'media/original.jpg'
registering = 'media/rotated.jpg'

warp_mtx = 'warp_mtx.npy'

# ----------------------------- Get fixed points ----------------------------- #
points = [[1663.2937, 3012.0159],
 [1599.8312, 2873.5522],
 [1063.2842, 2766.8198],
 [1060.3995, 2469.6997],
 [1620.0238, 2412.0066],
 [1692.1403, 2296.62  ]]
# points = get_fixed_points(reference)


# --------------------------------- Register --------------------------------- #
register(reference, registering, fixed_points = points)

# 3.4.1.15 in setup
# TODO implement affine calculation without using opencv because I hate it. 
# TODO change number of point requirement
# TODO test