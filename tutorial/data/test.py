from arenaregistration.register import register
from arenaregistration.points import get_fixed_points

reference = 'tutorial/data/original.jpg'
registering = 'tutorial/data/rotated.jpeg'

# ----------------------------- Get fixed points ----------------------------- #

# points = [(280, 201), (373, 199), (559, 332), (554, 565), (373, 585), (280, 583)] # ! ponts are defined as (y, x) tuples

# points = [[284.53525 203.6975 ],
#         [681.43176 382.51898],
#         [280.17377 585.32874]]
points = get_fixed_points(reference)


# --------------------------------- Register --------------------------------- #
register(reference, registering, fixed_points = points)

 # TODO allow for user to pass img as arrays instead of filepaths
 # TODO docs, docstrings, examples, tutorials...
