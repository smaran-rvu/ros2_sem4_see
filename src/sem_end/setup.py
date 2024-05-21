from setuptools import find_packages, setup

package_name = 'sem_end'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='smaran',
    maintainer_email='smaran@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "robot_motion_controller = sem_end.robot_motion_controller:main",
            "robot_motion_controller2 = sem_end.robot_motion_controller_2:main"
        ],
    },
)
