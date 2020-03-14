
from arenaregistration.points import get_registering_points
from arenaregistration.affine import apply_affine, affine_visualise_results


        

def register(reference_img, registering_img, fixed_points):
    if len(fixed_points) < 3:
        raise ValueError(f"Insufficient number of fixed points passed. It was {len(fixed_points)} but minimum is 3!")
    reference = load_image(reference_img)
    registering = load_image(registering_img)

    registering_points = get_registering_points(reference, registering, fixed_points)

    transformed, overlay = apply_affine(reference_img, registering_img, fixed_points, registering_points)

    affine_visualise_results(overlay, transformed)





