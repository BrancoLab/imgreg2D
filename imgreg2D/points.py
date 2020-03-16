import napari
import numpy as np


from imgreg2D import N_POINTS, POINTS_SIZE, EDGE_WIDTH
from imgreg2D.utils import load_image



# ----------------------------------- Utils ---------------------------------- #
def clean_check_points(points_layer=None, points=None, img_type='Fixed', verbose=True):
    if points_layer is not None:
        points = np.float32([list(p) for p in points_layer.data])
    elif points is not None: # exects a list of lists/typles with points 
        points = np.float32([p for p in points])
    else:
        raise ValueError('Neither points_layer nor points was passed')

    if len(points) < N_POINTS:
        raise ValueError(f'Found {len(points)} {img_type} points but a minimum of {N_POINTS} is required.')
    elif len(points) > N_POINTS:
        raise ValueError(f'Found {len(points)} {img_type} points but a maximum of {N_POINTS} is required.')
    else:
        if verbose:
            print(f"{img_type} points: {points}")
    return points

def invert_xy_order(points):
    return points[:, ::-1]



# ------------------------------- Fixed Points ------------------------------- #
def get_fixed_points(reference):
    print(f"\n\nDefine {N_POINTS} fixed points on reference image.\n"+
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
            point, n_points = layer.data[-1].astype(np.int32), len(layer.data)
            print(f"    added point ({point}). Tot points: {n_points}")
            if n_points == N_POINTS:
                close_viewer(reference_viewer)

    return clean_check_points(points_layer)


# ---------------------------- Registering Points ---------------------------- #
def get_registering_points(reference, registering, fixed_points):
    print(f"\n\nStarting registration: click on the points in the registering image"+
            "that match those on the reference image.\n"+
            "Press 'r' to toggle between seeing the reference or the registering image\n"+
            "Press 'q' to close the viewers.")

    with napari.gui_qt():
        # add the registering image
        registering_viewer = napari.view_image(registering, name='registering', title='Registering points')
        registering_viewer.window._qt_window.showFullScreen() 

        # User input -> points
        points_layer = registering_viewer.add_points(size=POINTS_SIZE, edge_color='k',
                    edge_width=EDGE_WIDTH, face_color='springgreen', name='registering_points')
        points_layer.mode = 'add'
        

        # add the reference image image
        registering_viewer.add_image(reference, name='reference image', visible=False)
        registering_viewer.add_points(fixed_points, size=POINTS_SIZE, edge_color='k',
                                    edge_width=EDGE_WIDTH, face_color='red', name='reference points',
                                    visible=False)

        reference_layers = [registering_viewer.layers[0], registering_viewer.layers[1]]
        registering_layers = [registering_viewer.layers[2], registering_viewer.layers[3]]
        registering_viewer.layers[0].metadata['viewing'] = 'registering'

        registering_viewer.active_layer = points_layer
        registering_viewer.cursor = 'pointing'

        # Add keybindings
        @napari.Viewer.bind_key('q', overwrite=True)
        def close_viewer(viewer):
            # registering_viewer.window._qt_window.showNormal()
            registering_viewer.close()

        @napari.Viewer.bind_key('r', overwrite=True)
        def toggle_reference(viewer):
            if registering_viewer.layers[0].metadata['viewing'] == 'registering':
                for layer in reference_layers: layer.visible = False
                for layer in registering_layers: layer.visible = True
                registering_viewer.layers[0].metadata['viewing'] = 'reference'
                viewer.status_message = 'REFERENCE IMAGE'
            else:
                for layer in reference_layers: layer.visible = True
                for layer in registering_layers: layer.visible = False
                registering_viewer.layers[0].metadata['viewing'] = 'registering'
                viewer.status_message = 'REGISTERING IMAGE'
                points_layer.mode = 'add'
                registering_viewer.active_layer = points_layer
                registering_viewer.cursor = 'pointing'

        @points_layer.mouse_drag_callbacks.append
        def check_n_points(layer, event):
            if registering_viewer.layers[0].metadata['viewing'] == 'reference':
                return

            if len(layer.data) == len(fixed_points):
                close_viewer(registering_viewer)

    if not len(points_layer.data) == len(fixed_points):
        raise ValueError(f"{len(points_layer.data)} were clicked, but there were {len(fixed_points)} on the reference image.\n"+
                            "Please try again.")
    
    return clean_check_points(points_layer, img_type='Registering')[::-1] # ? need to reverse the order for some reason