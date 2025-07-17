ROS2 Hand Gesture Recognition

A real-time hand gesture recognition system built with ROS2 and MediaPipe that detects hand gestures from camera input and publishes them to ROS topics for robotics applications.

Features:


1.Real-time gesture recognition using MediaPipe's gesture recognition model

2.Visual feedback with hand landmark visualization and confidence scores

3.ROS2 integration publishing detected gestures to /hand_gesture topic

4.Robust detection with confidence thresholding and debouncing

5.Live camera feed with OpenCV visualization

6.Dual API approach using both MediaPipe Tasks and Solutions APIs for optimal performance

7.Error handling with graceful camera initialization and cleanup


Supported Gestures

Currently detects:

*Closed_Fist - Closed fist gesture

*Open_Palm - Open palm gesture


Perfect for basic robot control commands (stop/go, grab/release, etc.)

Requirements:

System Dependencies:

1.ROS2 (Humble/Iron recommended)

2.Python 3.8+

3.Webcam/USB camera

4.Ubuntu 20.04/22.04 (recommended)
