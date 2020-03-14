import napari
from wand.image import Image
from wand.color import Color
from wand.display import display

from arenaregistration.utils import load_image

def apply_affine(reference_img, registering_img, fixed_points, registering_points):
    # The affine takes a list of integers such that you have [x_1_A, y_1_A, x_1_B, y_1_B...]
    # i.e. the coordinate for the first point in the first image, second image, second point in first image...
    # see: http://docs.wand-py.org/en/0.5.9/guide/distortion.html#affine
    print("\nApplying affine transform.")
    reg_params = []
    for p_a, p_b in zip(registering_points, fixed_points):
        reg_params.extend([int(p) for p in [*p_a, *p_b]])

    with Image(filename=reference_img) as ref: # reference image
        with Image(filename=registering_img) as reg: # Image to register
            with Image(filename=registering_img) as composite: # Used to show overlay between the two
                # Apply affine
                reg.distort('affine', reg_params)
                composite.distort('affine', reg_params)

                # Overlay
                composite.composite(ref, 0, 0, 'overlay')

                # Save results
                reg.save(filename='registered.png')
                composite.save(filename='composite.png')
    
    return load_image('registered.png'), load_image('composite.png')


def affine_visualise_results(overlay, transformed):
    print(f"\nVisualising results: overlayed images."
            "Press 'q' to close the viewers.")

    with napari.gui_qt():
        viewer = napari.view_image(overlay, name='Overlay')

        viewer.add_image(transformed, name='Transformed', visible=False)

        @viewer.bind_key('q', overwrite=True)
        def close_viewers(viewer):
            viewer.window.close()