"""
Configuration file for Cow Mastitis Detection System
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.absolute()

# Flask configuration
SECRET_KEY = 'your-secret-key-change-in-production-2024'
DEBUG = True

# Database configuration
DATABASE_PATH = BASE_DIR / 'mastitis_detection.db'

# Upload configuration
UPLOAD_FOLDER = BASE_DIR / 'uploads'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Model configuration
MODEL_PATH = BASE_DIR / 'yolov5_best_mastitis_detection.pt'
CONFIDENCE_THRESHOLD = 0.25  # Minimum confidence for detections

# Severity mapping configuration
# Maps YOLO class names to severity levels
SEVERITY_MAPPING = {
    'udder_normal': 'Mastitis-No',
    'thermal_udder_normal': 'Mastitis-No',
    'thermal_healthy_cow': 'Mastitis-No',
    'thermal_suspected_cow': 'Mastitis-Low',
    'mastitis_infected_udder': 'Mastitis-Moderate',  # Will be split by confidence
    'thermal_udder_mastitis': 'Mastitis-High',
}

# Confidence thresholds for splitting infected udder severity
HIGH_SEVERITY_CONFIDENCE = 0.7  # >= 0.7 is High, < 0.7 is Moderate

# Severity colors for UI
SEVERITY_COLORS = {
    'Mastitis-No': '#10B981',      # Green
    'Mastitis-Low': '#F59E0B',     # Yellow/Amber
    'Mastitis-Moderate': '#EF4444', # Orange/Red
    'Mastitis-High': '#DC2626',     # Dark Red
}

# Create necessary directories
UPLOAD_FOLDER.mkdir(exist_ok=True)
(UPLOAD_FOLDER / 'images').mkdir(exist_ok=True)
(UPLOAD_FOLDER / 'videos').mkdir(exist_ok=True)
(UPLOAD_FOLDER / 'results').mkdir(exist_ok=True)
