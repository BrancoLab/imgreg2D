# Imgreg2D
Simple napari based python application to register a 2D image to a template. 


## Installation
You can instal the code directly from Pypi using:

```
pip install imgreg2d
```

Alternative you can instal directly from the ![github repository](https://github.com/BrancoLab/imgreg2D) with:
```
pip install git+https://github.com/BrancoLab/imgreg2D.git --upgrade
```

## USAGE
To register an image to a template the user needs to specify the location of a set of points (>3, ideally at least 6) on 
both the reference and the registering image. These data are then used to compute an affine matrix which is then used to 
warp the registering image so that it matches the template. 

For an example of how to perfom image registration, check `example.py` or read below:

### Step 0 - import function and get the images
```
from imgreg2D.register import register
from imgreg2D.points import get_fixed_points

reference = 'media/original.jpg' # <- path to reference image
registering = 'media/rotated.jpg' # <- path to registering image
```

When we will call `register` we will have to pass the the reference and registering images. 
This can be done by passing file paths like in the code above or by passing `np.ndarray` with image data.


### Step 1 - define points on reference image
To define the location of the points used for registration on the reference image (`fixed_points`) you can use
`get_fixed_points`. If you already know the location of these points (e.g. because you already used the same
template image), you can skip this step. 

```
points = get_fixed_points(reference)
```

Once you've clicked on all the points you need, press `q` to close the viewer and proceed to the next step. 

### Step 2 - define points on registering image
Now you will have to click on the corresponding set of points in the registering image so that the 
affine transform can be computed. Remember, the order in which the points are defined is important: the first point
you clicked in Step 1 has to correspond to the first point you'll define now. For this reason, you're shown a copy
of your reference image with the location and sequence of fixed points. Once you've defined all the registering points
the editor will close automatically and the analysis will proceed to the next step. 

To start defining the registering points call:
```
register(reference, registering, fixed_points = points)
```

Note: if you already have a transform matrix (e.g. from a previous run of the registering step), you can skip this step.
To skip Step 2 simply call:

```
warped_img, warp_mtx = register(reference, registering, warp_mtx = warp_mtx)
```

Note2: when calling register you can decide if you want to save the warp matrix or not. This could be use to save time
the next time you need to register an image. 


### Step 3 - interactive refinement
Once you've defined the location of the registering points, the code will compute the affine transform (`warp_mtx`) and 
register your image. 
At this point another napari viewer will open which you can use to refine the accuracy of your transformation using the
following hotkeys:

```
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
##    SCALING                                            ##
##   ------------------------------------------------     ##
##      'r' -> positive x scaling                         ##
##      'f' -> negative x scaling                         ##
##                                                        ##
##      't' -> positive y scaling                         ##
##      'g' -> negative y scaling                         ##
##                                                        ##
##    SHEARS                                              ##
##   ------------------------------------------------     ##
##      'z' -> positive x shear                           ##
##      'x' -> negative x shear                           ##
##                                                        ##
##      'c' -> positive y shear                           ##
##      'v' -> negative y shear                           ##
##                                                        ##
############################################################
```

Once you're happy with your results, press `y` to complete the analysis (if you're not happy, 
press `n` and you can try again from Step 2).
After Step 3 you'll have your registered image (`warped_img`) and your affine transform matrix (`warp_mtx`), enjoy!



# Credit and contribution
The original code was part of [Common-Coordinates-Behaviour](https://github.com/BrancoLab/Common-Coordinate-Behaviour) (credit: Philip Shamash). The code was adapted to work with Napari.

Contributions are welcome! Just send a PR or open an issue as neeeded. 



