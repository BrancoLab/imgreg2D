from arenaregistration import N_POINTS
from arenaregistration.points import get_registering_points, get_fixed_points, clean_check_points
from arenaregistration.affine import apply_affine, affine_visualise_results, get_affine_matrix
from arenaregistration.utils import load_image




def register(reference_img, registering_img, fixed_points=None, warp_mtx=None):
    def get_points():
        if fixed_points is None:
            fixed_points = get_fixed_points(reference_img)
        else:
            fixed_points = clean_check_points(points=fixed_points, verbose=False)

    if warp_mtx is None:
        get_points()

    reference = load_image(reference_img)
    registering = load_image(registering_img)

    happy = False
    while not happy: # keep repeating process until happy
        if warp_mtx is None:
            # Get registration points
            registering_points = get_registering_points(reference, registering, fixed_points)
            warp_mtx = get_affine_matrix(fixed_points, registering_points)

        # Get registered image
        registered = apply_affine(reference, registering)

        # Visualise results
        happy = affine_visualise_results(reference, registered)

        if happy == 'stop':
            print("\nStopping")
            break
        elif not happy:
            print("\nYou're not happy with the results... trying again!")
            warp_mtx = None
        else:
            print("\nRegistration completed! Saving the results.")




