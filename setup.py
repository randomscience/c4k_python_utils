from setuptools import find_packages, setup

metadata = dict(
    name="c4k_python_utils",
    version="0.1.8",
    packages=["c4k_python_utils"],
    install_requires=[
        "numpy",
        "opencv-python",
        "matplotlib",
        "tensorflow",
        "scipy",
        "pymongo",
        "imageio",
        "boto3",
        "computer_vision_utils @ git+https://github.com/mateuszkojro/computer_vision_utils",
    ],
)

setup(**metadata)
