from arenaregistration.register import register
from arenaregistration.points import get_fixed_points

reference = 'media/original.jpg'
registering = 'media/rotated.jpg'

warp_mtx = 'warp_mtx.npy'

# ----------------------------- Get fixed points ----------------------------- #
points = get_fixed_points(reference)


# --------------------------------- Register --------------------------------- #
register(reference, registering, fixed_points = points)

