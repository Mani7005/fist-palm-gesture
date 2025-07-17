import rclpy
import cv2
import time
import pathlib
import mediapipe as mp
from rclpy.node import Node
from std_msgs.msg import String
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = str(pathlib.Path.home() / "models/gesture_recognizer.task")

class GesturePublisher(Node):
    def __init__(self):
        super().__init__("gesture_publisher")
        self.publisher = self.create_publisher(String, "/hand_gesture", 10)
        
       
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        
        
        self.hands_detector = self.mp_hands.Hands(
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error("Failed to open camera!")
            return
            
        self.last_label = None
        self.last_time = time.time()
        
        
        self.latest_gesture_result = None
        
       
        try:
            base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
            options = vision.GestureRecognizerOptions(
                base_options=base_options,
                running_mode=vision.RunningMode.LIVE_STREAM,
                result_callback=self.gesture_callback,
                num_hands=1
            )
            self.recognizer = vision.GestureRecognizer.create_from_options(options)
            self.get_logger().info("Gesture recognizer initialized successfully")
        except Exception as e:
            self.get_logger().error(f"Failed to initialize gesture recognizer: {e}")
            return
    
    def gesture_callback(self, result: vision.GestureRecognizerResult, image, timestamp_ms: int):
       
        self.latest_gesture_result = result
        
        if not result.gestures:
            return
            
       
        gesture = result.gestures[0][0]
        label = gesture.category_name
        confidence = gesture.score
        
       
        self.get_logger().info(f"Detected: {label} (confidence: {confidence:.2f})")
        
        
        if confidence > 0.6 and label in ("Closed_Fist", "Open_Palm"):
            current_time = time.time()
            
           
            if label != self.last_label or current_time - self.last_time > 0.5:
                msg = String()
                msg.data = label
                self.publisher.publish(msg)
                self.get_logger().info(f"Published: {label}")
                
                self.last_label = label
                self.last_time = current_time
    
    def loop(self):
        success, image = self.cap.read()
        if not success:
            self.get_logger().error("Failed to read from camera.")
            return False
        
       
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        
        hands_results = self.hands_detector.process(image)
        
        
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        
        if hands_results.multi_hand_landmarks:
            for hand_landmarks in hands_results.multi_hand_landmarks:
                # This is the standard way - same as sample code
                self.mp_drawing.draw_landmarks(
                    image, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
        
        
        rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp = int(time.time() * 1000)
        
        
        self.recognizer.recognize_async(mp_image, timestamp)
        
        
        if self.latest_gesture_result and self.latest_gesture_result.gestures:
            gesture = self.latest_gesture_result.gestures[0][0]
            text = f"{gesture.category_name}: {gesture.score:.2f}"
            cv2.putText(image, text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        
        cv2.imshow("Hand Gesture Recognition", image)
        
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key
            self.get_logger().info("ESC pressed, shutting down...")
            return False
            
        return True

def main():
    rclpy.init()
    
    try:
        node = GesturePublisher()
        
        
        while rclpy.ok():
           
            rclpy.spin_once(node, timeout_sec=0.01)
            
           
            if not node.loop():
                break
                
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
       
        if 'node' in locals():
            node.cap.release()
            cv2.destroyAllWindows()
            node.destroy_node()
        rclpy.shutdown()
