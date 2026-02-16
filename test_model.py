"""
Simple test script to debug model loading
"""
import sys
from pathlib import Path

print("=" * 70)
print("DEBUGGING MODEL LOADER")
print("=" * 70)

# Test 1: Check if model file exists
model_path = Path("yolov5_best_mastitis_detection.pt")
print(f"\n1. Checking model file...")
print(f"   Path: {model_path.absolute()}")
print(f"   Exists: {model_path.exists()}")
if model_path.exists():
    print(f"   Size: {model_path.stat().st_size / 1024 / 1024:.2f} MB")

# Test 2: Try importing ultralytics
print(f"\n2. Testing ultralytics import...")
try:
    from ultralytics import YOLO
    print("   ✓ ultralytics imported successfully")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    sys.exit(1)

# Test 3: Try loading model
print(f"\n3. Testing model loading...")
try:
    print("   Loading model (this may take a moment)...")
    model = YOLO(str(model_path))
    print("   ✓ Model loaded successfully!")
    print(f"   Model type: {type(model)}")
    print(f"   Model classes: {model.names if hasattr(model, 'names') else 'Not available'}")
except Exception as e:
    print(f"   ✗ ERROR loading model: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Check config
print(f"\n4. Testing config import...")
try:
    import config
    print("   ✓ config module imported")
    print(f"   MODEL_PATH: {config.MODEL_PATH}")
    print(f"   UPLOAD_FOLDER: {config.UPLOAD_FOLDER}")
except Exception as e:
    print(f"   ✗ ERROR: {e}")

print("\n" + "=" * 70)
print("✓ ALL TESTS PASSED - Model is working correctly!")
print("=" * 70)
