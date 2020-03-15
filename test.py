from arenaregistration.register import register
from arenaregistration.points import get_fixed_points

reference = 'tutorial/data/original.jpg'
registering = 'tutorial/data/rotated.jpg'

# ----------------------------- Get fixed points ----------------------------- #
points = get_fixed_points(reference)


# --------------------------------- Register --------------------------------- #
register(reference, registering, fixed_points = points)

# TODO points ordering + labels
# TODO docs, docstrings, examples, tutorials...
# TODO handle saving / loading of mtx

# TODO add get inverse matrix