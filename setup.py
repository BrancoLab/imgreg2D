from setuptools import setup, find_namespace_packages

requirements = [
    "numpy",
    "opencv-python",
    "nptdms",
    "configparser",
    "pandas",
    "tqdm",

]

setup(
    name="FC_analysis",
    version="0.0.0.1",
    author_email="federicoclaudi@protonmail.com",
    description="Code to analyse stuff",
    packages=find_namespace_packages(exclude=()),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "dlc_on_hpc = analysis.dbase.tracking.track_hpc:main",
        ]
    },
    url="https://github.com/BrancoLab/FC_analysis",
    author="Federico Claudi",
    zip_safe=False,
)
