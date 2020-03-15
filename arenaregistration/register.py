from arenaregistration import N_POINTS
from arenaregistration.points import get_registering_points, get_fixed_points, clean_check_points
from arenaregistration.affine import apply_affine, affine_visualise_results, get_affine_matrix
from arenaregistration.utils import load_image




def register(reference, registering, fixed_points=None, warp_mtx=None, save_mtx=False,
                save_fld='', save_name='warp_mtx'):
    if isinstance(reference, str): # images were passed as filepaths
        # Load reference and registering images from file
        reference = load_image(reference)
        registering = load_image(registering)
   
    if warp_mtx is None:
        if fixed_points is None:
            fixed_points = get_fixed_points(reference)
        else:
            fixed_points = clean_check_points(points=fixed_points, verbose=False)

    happy = False
    while not happy: # keep repeating process until happy
        if warp_mtx is None:
            # Get registration points
            registering_points = get_registering_points(reference, registering, fixed_points)
            warp_mtx = get_affine_matrix(fixed_points, registering_points)

        # Get registered image
        registered = apply_affine(reference, registering, warp_mtx)

        # Visualise results
        happy = affine_visualise_results(reference, registered)

        # Check if we need to try again
        if happy == 'stop':
            print("\nStopping")
            break
        elif not happy:
            print("\nYou're not happy with the results... trying again!")
            warp_mtx = None
        else:
            print("\nRegistration completed! Saving the results.")




