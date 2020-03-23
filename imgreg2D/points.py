import napari
import numpy as np
import cv2

from imgreg2D import MIN_N_POINTS, POINTS_SIZE, EDGE_WIDTH
from imgreg2D.utils import load_image, create_marked_ref_image


# ----------------------------------- Utils ---------------------------------- #
def clean_check_points(points, img_type='Fixed', verbose=True):
    points = np.float32(points)

    if len(points) < MIN_N_POINTS:
        raise ValueError(f'Found {len(points)} {img_type} points but a minimum of {MIN_N_POINTS} is required.')

    else:
        if verbose:
            print(f"{img_type} points:\n{points}")

    return points

def invert_xy_order(points):
    return points[:, ::-1]

# ------------------------------- Fixed Points ------------------------------- #
def get_fixed_points(reference):
    print(f"\n\nDefine at least {MIN_N_POINTS} fixed points on reference image.\n"+
            "Press 'q' to close viewer when all the points are defined")

    if isinstance(reference, str):
        reference = load_image(reference)

    with napari.gui_qt() as gui:
        reference_viewer = napari.view_image(reference, title='Get Fixed Points', name='reference')
        reference_viewer.window._qt_window.showFullScreen()

        points_layer = reference_viewer.add_points(size=POINTS_SIZE, edge_color='k',
                                    edge_width=EDGE_WIDTH, face_color='red', name='fixed_points')
        points_layer.mode = 'add'

        # Add keybindings
        @reference_viewer.bind_key('q', overwrite=True)
        def close_viewer(viewer):
            # Close viewer
            viewer.close()


        @points_layer.mouse_drag_callbacks.append
        def _print(layer, event):
            point, MIN_N_POINTS = layer.data[-1].astype(np.int32), len(layer.data)
            print(f"    added point ({point}). Tot points: {MIN_N_POINTS}")

    points = [list(p) for p in clean_check_points(points_layer.data)]
    print(f"{len(points)} points were defined.\n")
    return points


# ---------------------------- Registering Points ---------------------------- #
def get_registering_points(reference, registering, fixed_points):
    print(f"\n\nStarting registration: click on the points in the registering image"+
            "that match those on the reference image.\n"+
            "Press 'q' to close the viewers.")

    # Crete reference image with marked points
    reference_marked = create_marked_ref_image(reference.copy(), fixed_points)

    # Reshape registering image to reference image shape
    cols, rows, chs = reference.shape
    registering = cv2.resize(registering, (rows, cols))

    with napari.gui_qt():
        # add the registering image
        registering_viewer = napari.view_image(registering, name='registering', title='Registering points')
        # registering_viewer.window._qt_window.showFullScreen() 
        registering_viewer.cursor = 'pointing'

        # User input -> points
        points_layer = registering_viewer.add_points(size=POINTS_SIZE, edge_color='k',
                    edge_width=EDGE_WIDTH, face_color='springgreen', name='registering_points')
        points_layer.mode = 'add'
        registering_viewer.active_layer = points_layer
        registering_viewer.cursor = 'pointing'

        # create a viewer for the reference image image
        reference_viewer = napari.view_image(reference_marked, name='reference', title='Fixed points')
        viewers = [reference_viewer, registering_viewer]

        # Add keybindings
        @napari.Viewer.bind_key('q', overwrite=True)
        def close_viewer(viewer):
            for viewer in viewers:
                viewer.close()


        @points_layer.mouse_drag_callbacks.append
        def check_MIN_N_POINTS(layer, event):
            if len(points_layer.data) == len(fixed_points):
                for viewer in viewers:
                    viewer.close()

    if not len(points_layer.data) == len(fixed_points):
        raise ValueError(f"{len(points_layer.data)} were clicked, but there were {len(fixed_points)} on the reference image.\n"+
                            "Please try again.")
    
    return clean_check_points(points_layer.data, img_type='Registering')[::-1] # ? need to reverse the order for some reason