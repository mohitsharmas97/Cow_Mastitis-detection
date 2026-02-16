"""
YOLO Model loader and inference for Cow Mastitis Detection
"""
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import config


class MastitisDetector:
    """Mastitis detection using YOLOv5 model"""
    
    def __init__(self):
        """Initialize the YOLO model"""
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained YOLOv5 model"""
        try:
            print(f"Loading model from: {config.MODEL_PATH}")
            self.model = YOLO(str(config.MODEL_PATH))
            print("✓ Model loaded successfully")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            raise
    
    def classify_severity(self, class_name, confidence):
        """
        Classify severity based on detected class and confidence
        
        Args:
            class_name (str): YOLO detected class name
            confidence (float): Detection confidence
        
        Returns:
            str: Severity level
        """
        # Check if it's mastitis infected udder - split by confidence
        if class_name == 'mastitis_infected_udder':
            if confidence >= config.HIGH_SEVERITY_CONFIDENCE:
                return 'Mastitis-High'
            else:
                return 'Mastitis-Moderate'
        
        # Use mapping for other classes
        return config.SEVERITY_MAPPING.get(class_name, 'Mastitis-Moderate')
    
    def detect_image(self, image_path, output_path):
        """
        Perform detection on a single image
        
        Args:
            image_path (str): Path to input image
            output_path (str): Path to save annotated image
        
        Returns:
            dict: Detection results
        """
        # Run inference
        results = self.model(image_path, conf=config.CONFIDENCE_THRESHOLD)
        
        # Get the first result
        result = results[0]
        
        # Extract detection information
        detections = []
        severity_counts = {
            'Mastitis-No': 0,
            'Mastitis-Low': 0,
            'Mastitis-Moderate': 0,
            'Mastitis-High': 0
        }
        
        if len(result.boxes) > 0:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = result.names[class_id]
                
                # Classify severity
                severity = self.classify_severity(class_name, confidence)
                severity_counts[severity] += 1
                
                detections.append({
                    'class': class_name,
                    'confidence': confidence,
                    'severity': severity,
                    'bbox': box.xyxy[0].tolist()
                })
        
        # Determine overall severity (worst case)
        overall_severity = 'Mastitis-No'
        max_confidence = 0.0
        
        if severity_counts['Mastitis-High'] > 0:
            overall_severity = 'Mastitis-High'
            max_confidence = max([d['confidence'] for d in detections if d['severity'] == 'Mastitis-High'])
        elif severity_counts['Mastitis-Moderate'] > 0:
            overall_severity = 'Mastitis-Moderate'
            max_confidence = max([d['confidence'] for d in detections if d['severity'] == 'Mastitis-Moderate'])
        elif severity_counts['Mastitis-Low'] > 0:
            overall_severity = 'Mastitis-Low'
            max_confidence = max([d['confidence'] for d in detections if d['severity'] == 'Mastitis-Low'])
        elif severity_counts['Mastitis-No'] > 0:
            overall_severity = 'Mastitis-No'
            max_confidence = max([d['confidence'] for d in detections if d['severity'] == 'Mastitis-No'])
        
        # Save annotated image
        annotated_img = result.plot()
        cv2.imwrite(str(output_path), annotated_img)
        
        return {
            'detections': detections,
            'total_detections': len(detections),
            'severity': overall_severity,
            'confidence': max_confidence,
            'severity_counts': severity_counts,
            'annotated_path': str(output_path)
        }
    
    def detect_video(self, video_path, output_path, sample_rate=30):
        """
        Perform detection on a video (sample frames)
        
        Args:
            video_path (str): Path to input video
            output_path (str): Path to save annotated video
            sample_rate (int): Process every Nth frame
        
        Returns:
            dict: Aggregated detection results
        """
        cap = cv2.VideoCapture(str(video_path))
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        # Aggregated results
        all_detections = []
        severity_counts = {
            'Mastitis-No': 0,
            'Mastitis-Low': 0,
            'Mastitis-Moderate': 0,
            'Mastitis-High': 0
        }
        
        frame_idx = 0
        processed_frames = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Process every Nth frame
            if frame_idx % sample_rate == 0:
                # Run inference on frame
                results = self.model(frame, conf=config.CONFIDENCE_THRESHOLD)
                result = results[0]
                
                # Extract detections
                if len(result.boxes) > 0:
                    for box in result.boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        class_name = result.names[class_id]
                        
                        severity = self.classify_severity(class_name, confidence)
                        severity_counts[severity] += 1
                        
                        all_detections.append({
                            'frame': frame_idx,
                            'class': class_name,
                            'confidence': confidence,
                            'severity': severity
                        })
                
                # Get annotated frame
                annotated_frame = result.plot()
                out.write(annotated_frame)
                processed_frames += 1
            else:
                # Write original frame
                out.write(frame)
            
            frame_idx += 1
        
        cap.release()
        out.release()
        
        # Determine overall severity
        overall_severity = 'Mastitis-No'
        max_confidence = 0.0
        
        if severity_counts['Mastitis-High'] > 0:
            overall_severity = 'Mastitis-High'
            max_confidence = max([d['confidence'] for d in all_detections if d['severity'] == 'Mastitis-High'])
        elif severity_counts['Mastitis-Moderate'] > 0:
            overall_severity = 'Mastitis-Moderate'
            max_confidence = max([d['confidence'] for d in all_detections if d['severity'] == 'Mastitis-Moderate'])
        elif severity_counts['Mastitis-Low'] > 0:
            overall_severity = 'Mastitis-Low'
            max_confidence = max([d['confidence'] for d in all_detections if d['severity'] == 'Mastitis-Low'])
        elif len(all_detections) > 0:
            max_confidence = max([d['confidence'] for d in all_detections])
        
        return {
            'detections': all_detections,
            'total_detections': len(all_detections),
            'total_frames': total_frames,
            'processed_frames': processed_frames,
            'severity': overall_severity,
            'confidence': max_confidence,
            'severity_counts': severity_counts,
            'annotated_path': str(output_path)
        }


# Global detector instance
detector = None

def get_detector():
    """Get or create detector instance"""
    global detector
    if detector is None:
        detector = MastitisDetector()
    return detector
