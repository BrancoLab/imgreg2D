from arenaregistration.register import register
from arenaregistration.points import get_fixed_points

reference = 'tutorial/data/original.jpg'
registering = 'tutorial/data/rotated.jpg'

warp_mtx = 'warp_mtx.npy'

# ----------------------------- Get fixed points ----------------------------- #
# points = get_fixed_points(reference)


# --------------------------------- Register --------------------------------- #
register(reference, registering, warp_mtx=warp_mtx)  # fixed_points = points)

# TODO docs, docstrings, examples, tutorials...
# TODO add get inverse matrixy