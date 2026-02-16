"""
Flask application for Cow Mastitis Detection System
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import os
from functools import wraps

import config
import database
from model_loader import get_detector
from recommendations import get_recommendations_text, format_recommendations_html

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE


# Helper functions
def allowed_file(filename, file_type):
    """Check if file has allowed extension"""
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    if file_type == 'image':
        return ext in config.ALLOWED_IMAGE_EXTENSIONS
    elif file_type == 'video':
        return ext in config.ALLOWED_VIDEO_EXTENSIONS
    
    return False


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash('All fields are required', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'danger')
            return render_template('register.html')
        
        # Add user to database
        success, message = database.add_user(username, email, password)
        
        if success:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'danger')
            return render_template('register.html')
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = database.authenticate_user(username, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    # Get recent history
    recent_history = database.get_user_history(session['user_id'], limit=5)
    
    return render_template('dashboard.html', recent_history=recent_history)


@app.route('/upload', methods=['POST'])
@login_required
def upload():
    """Handle file upload and detection"""
    print("\n" + "="*50)
    print("UPLOAD REQUEST RECEIVED")
    print("="*50)
    
    try:
        if 'file' not in request.files:
            print("ERROR: No file in request.files")
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        print(f"File received: {file.filename}")
        
        if file.filename == '':
            print("ERROR: Empty filename")
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Determine file type
        is_image = allowed_file(file.filename, 'image')
        is_video = allowed_file(file.filename, 'video')
        print(f"File type - Image: {is_image}, Video: {is_video}")
        
        if not (is_image or is_video):
            print("ERROR: Invalid file type")
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = Path(filename).stem + f"_{session['user_id']}_{os.urandom(4).hex()}" + Path(filename).suffix
        
        media_type = 'image' if is_image else 'video'
        upload_folder = config.UPLOAD_FOLDER / (media_type + 's')
        filepath = upload_folder / timestamp
        
        print(f"Saving file to: {filepath}")
        file.save(filepath)
        print(f"✓ File saved successfully")
        
        # Run detection
        print(f"Starting detection...")
        detector = get_detector()
        print(f"✓ Detector loaded")
        
        # Output path
        output_filename = f"result_{timestamp}"
        output_path = config.UPLOAD_FOLDER / 'results' / output_filename
        
        print(f"Running model inference...")
        if is_image:
            results = detector.detect_image(filepath, output_path)
        else:
            results = detector.detect_video(filepath, output_path)
        
        print(f"✓ Detection complete - Severity: {results['severity']}")
        
        # Get recommendations
        print(f"Generating recommendations...")
        recommendations_text = get_recommendations_text(results['severity'])
        recommendations_html = format_recommendations_html(results['severity'])
        print(f"✓ Recommendations generated")
        
        # Save to database
        print(f"Saving to database...")
        detection_id = database.save_detection(
            user_id=session['user_id'],
            filename=output_filename,
            media_type=media_type,
            severity=results['severity'],
            confidence=results['confidence'],
            detection_count=results['total_detections'],
            recommendations=recommendations_text
        )
        print(f"✓ Saved to database with ID: {detection_id}")
        
        response_data = {
            'success': True,
            'detection_id': detection_id,
            'severity': results['severity'],
            'confidence': round(results['confidence'] * 100, 2),
            'detection_count': results['total_detections'],
            'severity_counts': results['severity_counts'],
            'recommendations': recommendations_html,
            'result_filename': output_filename,
            'original_filename': timestamp,
            'media_type': media_type
        }
        
        print(f"✓ Request completed successfully")
        print("="*50 + "\n")
        return jsonify(response_data)
    
    except Exception as e:
        print(f"\n✗ ERROR in upload route:")
        print(f"  Error type: {type(e).__name__}")
        print(f"  Error message: {str(e)}")
        import traceback
        traceback.print_exc()
        print("="*50 + "\n")
        return jsonify({'success': False, 'error': f"{type(e).__name__}: {str(e)}"}), 500


@app.route('/history')
@login_required
def history():
    """Detection history page"""
    all_history = database.get_user_history(session['user_id'])
    
    return render_template('history.html', history=all_history)


@app.route('/download/<filename>')
@login_required
def download(filename):
    """Download annotated result"""
    filepath = config.UPLOAD_FOLDER / 'results' / filename
    
    if filepath.exists():
        return send_file(filepath, as_attachment=True)
    else:
        flash('File not found', 'danger')
        return redirect(url_for('history'))


@app.route('/view/<media_type>/<filename>')
@login_required
def view_file(media_type, filename):
    """View uploaded or result file"""
    if media_type == 'image':
        filepath = config.UPLOAD_FOLDER / 'images' / filename
    elif media_type == 'video':
        filepath = config.UPLOAD_FOLDER / 'videos' / filename
    elif media_type == 'result':
        filepath = config.UPLOAD_FOLDER / 'results' / filename
    else:
        return "Invalid media type", 404
    
    if filepath.exists():
        return send_file(filepath)
    else:
        return "File not found", 404


if __name__ == '__main__':
    print("=" * 70)
    print("🐄 COW MASTITIS DETECTION SYSTEM")
    print("=" * 70)
    print(f"Starting Flask server...")
    print(f"Model: {config.MODEL_PATH}")
    print(f"Database: {config.DATABASE_PATH}")
    print(f"Upload folder: {config.UPLOAD_FOLDER}")
    print("=" * 70)
    
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)
