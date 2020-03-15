import napari
import cv2

from arenaregistration.utils import load_image
from arenaregistration.points import invert_xy_order

# ----------------------------- Affine transfrom ----------------------------- #
def get_affine_matrix(fixed_points, registering_points):
    print("\nGetting affine transform.")
    fixed_points = invert_xy_order(fixed_points)
    registering_points = invert_xy_order(registering_points)
    warp_mtx = cv2.getAffineTransform(fixed_points, registering_points)
    return warp_mtx

def apply_affine(reference, registering, warp_mtx):
    print("\nApplying affine transform.")
    rows,cols,ch =  reference.shape
    registered = cv2.warpAffine(registering, warp_mtx, (cols, rows))
    return registered



# --------------------------------- Visualise -------------------------------- #
def affine_visualise_results(reference, registered):
    print(f"\nVisualising results: overlayed images.\n"+
            "Press 'y' if you are happy with the results.\n"+
            "Press 'n' if you are not happy with the results and would like to try again.\n"+
            "Press 's' if you are not happy with the results and would like to stop.")

    with napari.gui_qt():
        viewer = napari.view_image(reference, name='Reference', opacity=.5)
        img_layer = viewer.add_image(registered, name='Registered', opacity=.5)

        viewer.layers[0].metadata['happy'] = False

        @viewer.bind_key('y', overwrite=True)
        def ishappy(viewer):
            viewer.layers[0].metadata['happy'] = True
            viewer.window.close()

        @viewer.bind_key('n', overwrite=True)
        def unhappy(viewer):
            viewer.layers[0].metadata['happy'] = False
            viewer.window.close() 

        @viewer.bind_key('s', overwrite=True)
        def stop(viewer):
            viewer.layers[0].metadata['happy'] = 'stop'
            viewer.window.close() 

    return viewer.layers[0].metadata['happy']
