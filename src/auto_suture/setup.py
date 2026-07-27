from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'auto_suture'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        (
            'share/' + package_name,
            ['package.xml'],
        ),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py'),
        ),
        (
            os.path.join('share', package_name, 'config'),
            glob('config/*.yaml'),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jazmin',
    maintainer_email='ll23jl@leeds.ac.uk',
    description='Autonomous suturing package',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'Simulation_to_ECM = auto_suture.Simulation_to_ECM:main',
            'Needle_Poses = auto_suture.Needle_Poses:main',
            'Grasp_Needle = auto_suture.Grasp_Needle:main',
            'Needle_Driving = auto_suture.Needle_Driving:main',
        ],
    },
)