from arenaregistration.register import register
from arenaregistration.points import get_fixed_points

reference = '/Users/federicoclaudi/Desktop/original.png'
registering = '/Users/federicoclaudi/Desktop/rotated.png'

# ----------------------------- Get fixed points ----------------------------- #

# points = [(772, 1185), (767, 2617), (1308, 2621), (1303, 1180)] # ! ponts are defined as (y, x) tuples
points = get_fixed_points(reference)


# --------------------------------- Register --------------------------------- #
register(reference, registering, points)

 # TODO utility to define registering points,
 # TODO allow for user to pass img as arrays instead of filepaths
 # TODO docs, docstrings, examples, tutorials...
