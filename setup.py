from setuptools import setup, find_namespace_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

requirements = [
    "numpy",
    "opencv-python==3.4.1.15",
    "configparser",
    "napari",
    "affine6p",
]

setup(
    name="imgreg2D",
    version="0.0.0.2",
    author_email="federicoclaudi@protonmail.com",
    description="easy 2D image registration in python",
    packages=find_namespace_packages(exclude=()),
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    url="https://github.com/BrancoLab/imgreg2D",
    author="Federico Claudi, Philip Shamash",
    zip_safe=False,
)
