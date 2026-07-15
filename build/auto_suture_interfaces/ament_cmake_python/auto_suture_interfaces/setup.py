from setuptools import find_packages
from setuptools import setup

setup(
    name='auto_suture_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('auto_suture_interfaces', 'auto_suture_interfaces.*')),
)
