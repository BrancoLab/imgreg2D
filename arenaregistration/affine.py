import napari
import cv2
import numpy as np

from arenaregistration import N_POINTS, POINTS_SIZE, EDGE_WIDTH
from arenaregistration.utils import load_image
from arenaregistration.points import invert_xy_order


warp_mtx_indices = dict(
    x_translate = (0, 2),
    y_translate = (1, 2),
    x_shear = (0, 0),
    y_shear = (1, 1),
    x_scale = (0, 1),
    y_scale = (1, 0),
)

KEYBINGS = """
############################################################
##                REFINEMENT HOT KEYS                     ##
##                                                        ##
##    TRANSLATIONS                                        ##
##   ------------------------------------------------     ##
##      'a' -> negative x translation                     ##
##      'w' -> positive y translation                     ##
##                                                        ##
##      's' -> negative y translation                     ##
##      'd' -> positive x translation                     ##
##                                                        ##
##    SCALINGS                                            ##
##   ------------------------------------------------     ##
##      'r' -> positive x scaling                         ##
##      'f' -> negative x scaling                         ##
##                                                        ##
##      't' -> positive y scaling                         ##
##      'g' -> negative y scaling                         ##
##                                                        ##
##    SHEARS                                              ##
##   ------------------------------------------------     ##
##      'd' -> positive x shear                           ##
##      'd' -> negative x shear                           ##
##                                                        ##
##      'd' -> positive y shear                           ##
##      'd' -> negative y shear                           ##
##                                                        ##
############################################################
"""


# ----------------------------- Affine transfrom ----------------------------- #
def get_affine_matrix(fixed_points, registering_points):
    print("\nGetting affine transform.")
    fixed_points = invert_xy_order(fixed_points)
    registering_points = invert_xy_order(registering_points)
    warp_mtx = cv2.getAffineTransform(fixed_points, registering_points)
    return warp_mtx

def apply_affine(reference, registering, warp_mtx, verbose=True):
    if verbose: print("\nApplying affine transform.")
    rows,cols,ch =  reference.shape
    registered = cv2.warpAffine(registering, warp_mtx, (cols, rows))
    return registered



# --------------------------------- Refine  -------------------------------- #
def update(viewer, reference, registering, warp_mtx, idx, sign, fact):
    # Update mtx
    if sign == 'plus':
        warp_mtx[idx] += np.abs(warp_mtx[idx]) * fact
    else:
        warp_mtx[idx] -= np.abs(warp_mtx[idx]) * fact

    # Apply affine
    registered = apply_affine(reference, registering, warp_mtx, verbose=False)

    # Update img layer
    viewer.layers[1].data = registered

def refine_registration(reference, registering, registered, warp_mtx):
    print(f"\nVisualising results: overlayed images.\n"+
            "Press 'y' if you are happy with the results.\n"+
            "Press 'n' if you are not happy with the results and would like to try again.\n"+
            "Press 'q' if you are not happy with the results and would like to stop.")

    print(KEYBINGS)

    # ------------------------------- Set up viewer ------------------------------ #
    with napari.gui_qt():
        # Add img layers
        viewer = napari.view_image(reference, name='Reference', opacity=.5, title='Refine Affine')
        img_layer = viewer.add_image(registered, name='Registered', opacity=.5)
        viewer.layers[0].metadata['happy'] = False
        viewer.layers[0].metadata['warp_mtx'] = warp_mtx

        # ---------------------------- Viewer key bindings --------------------------- #
        # keybings - user decides outcome
        @viewer.bind_key('y', overwrite=True)
        def ishappy(viewer):
            viewer.layers[0].metadata['happy'] = True
            viewer.window.close()

        @viewer.bind_key('n', overwrite=True)
        def unhappy(viewer):
            viewer.layers[0].metadata['happy'] = False
            viewer.window.close() 

        @viewer.bind_key('q', overwrite=True)
        def stop(viewer):
            viewer.layers[0].metadata['happy'] = 'stop'
            viewer.window.close() 

        # ------------------------------ Refine keybings ----------------------------- #
        # Translations
        @viewer.bind_key('a', overwrite=True)
        def a(viewer):
            update(viewer, reference, registering, warp_mtx, 
                            warp_mtx_indices['x_translate'], 'minus',  .02)

        @viewer.bind_key('w', overwrite=True)
        def w(viewer):
            update(viewer, reference, registering, warp_mtx, 
                            warp_mtx_indices['y_translate'], 'minus',  .02)

        @viewer.bind_key('s', overwrite=True)
        def s(viewer):
            update(viewer, reference, registering, warp_mtx, 
                            warp_mtx_indices['y_translate'], 'plus',  .02)

        @viewer.bind_key('d', overwrite=True)
        def d(viewer):
            update(viewer, reference, registering, warp_mtx, 
                            warp_mtx_indices['x_translate'], 'plus',  .02)


        # axis scales
        @viewer.bind_key('r', overwrite=True)
        def r(viewer):
            update(viewer, reference, registering, warp_mtx, 
                            warp_mtx_indices['x_scale'], 'plus', .3)

        @viewer.bind_key('f', overwrite=True)
        def f(viewer):
            update(viewer, reference, registering, warp_mtx, 
                            warp_mtx_indices['x_scale'], 'minus', .3)

        @viewer.bind_key('t', overwrite=True)
        def t(viewer):
            update(viewer, reference, registering, warp_mtx, 
                            warp_mtx_indices['y_scale'], 'plus', .3)

        @viewer.bind_key('g', overwrite=True)
        def g(viewer):
            update(viewer, reference, registering, warp_mtx, 
                            warp_mtx_indices['y_scale'], 'minus', .3)


        # Shears
        @viewer.bind_key('z', overwrite=True)
        def z(viewer):
            update(viewer, reference, registering, warp_mtx, 
                            warp_mtx_indices['x_shear'], 'plus', .3)

        @viewer.bind_key('x', overwrite=True)
        def x(viewer):
            update(viewer, reference, registering, warp_mtx, 
                            warp_mtx_indices['x_shear'], 'minus', .3)

        @viewer.bind_key('c', overwrite=True)
        def c(viewer):
            update(viewer, reference, registering, warp_mtx, 
                            warp_mtx_indices['y_shear'], 'plus', .3)

        @viewer.bind_key('v', overwrite=True)
        def v(viewer):
            update(viewer, reference, registering, warp_mtx, 
                            warp_mtx_indices['y_shear'], 'minus', .3)

    return viewer.layers[0].metadata['happy'], warp_mtx
