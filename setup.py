from setuptools import setup

package_name = 'gesture_ros_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rumani',
    maintainer_email='rumani@todo.todo',
    description='ROS2 node for gesture recognition using MediaPipe',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hand_gesture_node = gesture_ros_bridge.hand_gesture_node:main',
        ],
    },
)

