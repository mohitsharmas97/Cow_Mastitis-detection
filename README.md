# Cow Mastitis Detection System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![YOLOv5](https://img.shields.io/badge/YOLOv5-Deep%20Learning-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Advanced AI-powered system for detecting and classifying cow mastitis using deep learning**

</div>

---

## Features

- **Image Analysis**: Upload cow udder images for instant AI-powered detection
- **Video Processing**: Analyze videos frame-by-frame for comprehensive detection  
- **4-Level Severity Classification**:
  - **Mastitis-No** (Healthy)
  - **Mastitis-Low** (Mild)
  - **Mastitis-Moderate** (Moderate)
  - **Mastitis-High** (Severe)
- **Treatment Recommendations**: Severity-specific treatment guidelines
- **Confidence Scores**: Detection accuracy percentage for each analysis
- **Annotated Results**: Download images/videos with bounding boxes
- **Detection History**: Track all detections with timestamps
- **Secure Authentication**: User registration and login system
- **Responsive Design**: Works on desktop, tablet, and mobile devices

---

## System Architecture

```
cow_mastitis/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── database.py                     # SQLite database operations
├── model_loader.py                 # YOLO model inference
├── recommendations.py              # Treatment recommendations engine
├── requirements.txt                # Python dependencies
├── yolov5_best_mastitis_detection.pt  # Trained YOLOv5 model
├── mastitis_detection.db           # SQLite database (auto-generated)
├── static/
│   ├── css/
│   │   └── style.css              # Custom styles
│   └── js/
│       └── main.js                # JavaScript utilities
├── templates/
│   ├── base.html                  # Base template
│   ├── index.html                 # Landing page
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── dashboard.html             # Main detection dashboard
│   └── history.html               # Detection history
└── uploads/                       # Uploaded and processed files
    ├── images/
    ├── videos/
    └── results/
```

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (optional)

### Step 1: Clone or Download

```bash
# If using Git
git clone <repository-url>
cd cow_mastitis

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Model File

Ensure `yolov5_best_mastitis_detection.pt` is in the root directory:

```bash
# Check if file exists
ls yolov5_best_mastitis_detection.pt
```

### Step 5: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

---

## Usage Guide

### 1. **Register an Account**
   - Navigate to `http://localhost:5000`
   - Click "Register" in the navigation bar
   - Fill in username, email, and password
   - Click "Register" button

### 2. **Login**
   - Click "Login" in the navigation bar
   - Enter your credentials
   - Click "Login"

### 3. **Upload Media for Detection**
   - Go to the Dashboard
   - Drag & drop or click to select a file
   - Supported formats:
     - Images: PNG, JPG, JPEG
     - Videos: MP4, AVI, MOV
   - Click "Analyze for Mastitis"

### 4. **View Results**
   - **Severity Level**: Color-coded badge (Green/Yellow/Orange/Red)
   - **Confidence Score**: Percentage with progress bar
   - **Detection Count**: Number of detections found
   - **Recommendations**: Treatment guidelines based on severity
   - **Annotated Media**: View/download results with bounding boxes

### 5. **Check History**
   - Click "History" in navigation
   - View all past detections
   - Filter by severity level
   - Download previous results
   - View detailed recommendations

---

##  Detection Severity Levels

| Level | Description | Class Mapping | Action Required |
|-------|-------------|---------------|-----------------|
| **Mastitis-No** | Healthy, no mastitis detected | `udder_normal`, `thermal_udder_normal`, `thermal_healthy_cow` | Continue routine monitoring |
| **Mastitis-Low** | Mild mastitis, early intervention | `thermal_suspected_cow` | Monitor closely, preventive measures |
| **Mastitis-Moderate** | Moderate infection | `mastitis_infected_udder` (confidence < 0.7) | **Veterinary consultation within 24 hours** |
| **Mastitis-High** | Severe infection | `mastitis_infected_udder` (confidence ≥ 0.7), `thermal_udder_mastitis` | **🚨 URGENT: Immediate veterinary care** |

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Model settings
MODEL_PATH = 'yolov5_best_mastitis_detection.pt'
CONFIDENCE_THRESHOLD = 0.25  # Minimum confidence for detections

# File upload limits  
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Severity thresholds
HIGH_SEVERITY_CONFIDENCE = 0.7  # For infected udder classification
```

---

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite (lightweight, serverless)
- **Deep Learning**: 
  - YOLOv5 (Ultralytics)
  - PyTorch
- **Computer Vision**: OpenCV
- **Frontend**:
  - HTML5, CSS3, JavaScript
  - Bootstrap 5
  - Bootstrap Icons
- **Security**: Werkzeug (password hashing)

---

## Model Information

- **Architecture**: YOLOv5 (You Only Look Once)
- **Classes**: 8 detection classes
  - cow, cow_herd, mastitis_infected_udder
  - thermal_healthy_cow, thermal_suspected_cow
  - thermal_udder_mastitis, thermal_udder_normal, udder_normal
- **Input Size**: 640x640 pixels
- **Confidence Threshold**: 0.25 (configurable)

---

## Troubleshooting

### Model Loading Error
**Problem**: "Error loading model"
**Solution**:
1. Verify `yolov5_best_mastitis_detection.pt` exists
2. Check file permissions
3. Ensure PyTorch is installed: `pip install torch torchvision`

### Upload Fails
**Problem**: "File upload failed"
**Solution**:
1. Check file size (\< 100MB)
2. Verify file format (PNG, JPG, JPEG, MP4, AVI, MOV)
3. Check `uploads/` directory permissions

### Database Error
**Problem**: "Database connection failed"
**Solution**:
1. Delete `mastitis_detection.db`
2. Restart application (database will be recreated)

### Port Already in Use
**Problem**: "Address already in use"
**Solution**:
```bash
# Change port in app.py (last line)
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

---

## API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/` | GET | Landing page | No |
| `/register` | GET, POST | User registration | No |
| `/login` | GET, POST | User login | No |
| `/logout` | GET | User logout | Yes |
| `/dashboard` | GET | Main detection interface | Yes |
| `/upload` | POST | Upload and detect media | Yes |
| `/history` | GET | View detection history | Yes |
| `/download/<filename>` | GET | Download result file | Yes |
| `/view/<type>/<filename>` | GET | View media file | Yes |

---

## Security Features

- **Password Hashing**: Werkzeug SHA-256 hashing
- **Session Management**: Flask secure sessions
- **File Validation**: Type and size checking
- **SQL Injection Protection**: Parameterized queries
- **User Isolation**: Data separated by user ID

---

