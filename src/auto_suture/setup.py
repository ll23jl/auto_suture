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
            glob('config/*'),
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
            'needle_position = auto_suture.needle_position_node:main',
            'tool_grasp_position = auto_suture.tool_grasp_position_node:main',
        ],
    },
)