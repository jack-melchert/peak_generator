from setuptools import setup
import sys

setup(
    name='peak_gen',
    version='0.0.1',
    url='https://github.com/jack-melchert/peak_generator',
    license='MIT',
    maintainer='Jackson Melchert',
    maintainer_email='melchert@stanford.edu',
    description='Peak generator for DSE project',
    packages=[
        "peak_gen",
    ],
    install_requires=[
        "peak",
        "mantle",
        "jsonpickle",
        "ast-tools"
    ],
    python_requires='>=3.6'
)
