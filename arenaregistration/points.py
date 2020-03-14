import napari
import numpy as np

from arenaregistration.utils import load_image


# ----------------------------------- Utils ---------------------------------- #
def clean_check_points(points_layer, img_type='Fixed'):
    points = [tuple(p.astype(np.int32)) for p in points_layer.data]

    if len(points) < e:
        raise ValueError(f'Found {len(points)} {img_type} points but a minimum of 4 is required.')
    else:
        print(f"{img_type} points: {points}")
    return points



# ------------------------------- Fixed Points ------------------------------- #
def get_fixed_points(reference_img):
    print(f"\n\nDefine fixed points on reference image.\n"+
            "Press 'q' to close viewer when all the points are defined")
    with napari.gui_qt():
        reference_viewer = napari.view_image(load_image(reference_img), name='reference')
        points_layer = reference_viewer.add_points(size=15, edge_color='k',
                    edge_width=1, face_color='red', name='fixed_points')
        points_layer.mode = 'add'

        # Add keybindings
        @reference_viewer.bind_key('q', overwrite=True)
        def close_viewer(viewer):
            viewer.window.close()

        @points_layer.mouse_drag_callbacks.append
        def _print(layer, event):
            point, n_points = layer.data[-1].astype(np.int32), len(layer.data)
            print(f"    added point ({point}). Tot points: {n_points}")

    return clean_check_points(points_layer)


# ---------------------------- Registering Points ---------------------------- #
def get_registering_points(reference, registering, fixed_points):
    print(f"\n\nStarting registration: get matched points."
            f"# {len(fixed_points)} fixed points passed.\n"+
            "Please click on the equivalent points on the registering image.\n"+
            "Press 't' to start tagging points on the registering image\n"+
            "Press 'q' to close the viewers.")

    with napari.gui_qt():
        # add the reference image
        reference_viewer = napari.view_image(reference, name='reference')

        # Fixed points
        reference_viewer.add_points(fixed_points, size=15, edge_color='k',
                    edge_width=1, face_color='red', name='fixed_points')

        # add the registering image
        registering_viewer = napari.view_image(registering, name='registering')

        # User input -> points
        points_layer = registering_viewer.add_points(size=15, edge_color='k',
                    edge_width=1, face_color='blue', name='registering_points')
        points_layer.mode = 'add'

        viewers = [reference_viewer, registering_viewer]

        # Add keybindings
        @napari.Viewer.bind_key('q', overwrite=True)
        def close_viewers(viewer):
            for viewer in viewers:
                viewer.window.close()

        @points_layer.mouse_drag_callbacks.append
        def check_n_points(layer, event):
            if len(layer.data) == len(fixed_points):
                for viewer in viewers:
                    viewer.window.close()

    if not len(points_layer.data) == len(fixed_points):
        raise ValueError(f"{len(points_layer.data)} were clicked, but there were {len(fixed_points)} on the reference image.\n"+
                            "Please try again.")
    
    return clean_check_points(points_layer, img_type='Registering')