ROS2 Hand Gesture Recognition
A real-time hand gesture recognition system built with ROS2 and MediaPipe that detects hand gestures from camera input and publishes them to ROS topics for robotics applications.
Features:

Real-time gesture recognition using MediaPipe's gesture recognition model
Visual feedback with hand landmark visualization and confidence scores
ROS2 integration publishing detected gestures to /hand_gesture topic
Robust detection with confidence thresholding and debouncing
Live camera feed with OpenCV visualization
Dual API approach using both MediaPipe Tasks and Solutions APIs for optimal performance
Error handling with graceful camera initialization and cleanup

Supported Gestures
Currently detects:

Closed_Fist - Closed fist gesture
Open_Palm - Open palm gesture

Perfect for basic robot control commands (stop/go, grab/release, etc.)
Requirements:
System Dependencies:

ROS2 (Humble/Iron recommended)
Python 3.8+
Webcam/USB camera
Ubuntu 20.04/22.04 (recommended)
