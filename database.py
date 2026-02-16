"""
Database operations for Cow Mastitis Detection System
"""
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import DATABASE_PATH


def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    """Initialize database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Detection history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            media_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            confidence REAL NOT NULL,
            detection_count INTEGER DEFAULT 0,
            recommendations TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()


def add_user(username, email, password):
    """
    Add a new user to the database
    
    Args:
        username (str): Unique username
        email (str): User's email
        password (str): Plain text password (will be hashed)
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Hash the password
        password_hash = generate_password_hash(password)
        
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        
        conn.commit()
        conn.close()
        return True, "User registered successfully"
    
    except sqlite3.IntegrityError:
        return False, "Username or email already exists"
    except Exception as e:
        return False, f"Registration failed: {str(e)}"


def authenticate_user(username, password):
    """
    Authenticate a user
    
    Args:
        username (str): Username
        password (str): Plain text password
    
    Returns:
        dict or None: User data if authenticated, None otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    user = cursor.execute(
        'SELECT * FROM users WHERE username = ?',
        (username,)
    ).fetchone()
    
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email']
        }
    
    return None


def save_detection(user_id, filename, media_type, severity, confidence, detection_count, recommendations):
    """
    Save a detection result to the database
    
    Args:
        user_id (int): User ID
        filename (str): Uploaded file name
        media_type (str): 'image' or 'video'
        severity (str): Detected severity level
        confidence (float): Detection confidence score
        detection_count (int): Number of detections in the media
        recommendations (str): Treatment recommendations
    
    Returns:
        int: Detection ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO detections 
        (user_id, filename, media_type, severity, confidence, detection_count, recommendations)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, filename, media_type, severity, confidence, detection_count, recommendations))
    
    detection_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return detection_id


def get_user_history(user_id, limit=None):
    """
    Get detection history for a user
    
    Args:
        user_id (int): User ID
        limit (int, optional): Limit number of results
    
    Returns:
        list: List of detection records
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT * FROM detections 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
    '''
    
    if limit:
        query += f' LIMIT {limit}'
    
    detections = cursor.execute(query, (user_id,)).fetchall()
    conn.close()
    
    return [dict(detection) for detection in detections]


def get_detection_by_id(detection_id, user_id):
    """
    Get a specific detection by ID (with user validation)
    
    Args:
        detection_id (int): Detection ID
        user_id (int): User ID for validation
    
    Returns:
        dict or None: Detection record
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    detection = cursor.execute(
        'SELECT * FROM detections WHERE id = ? AND user_id = ?',
        (detection_id, user_id)
    ).fetchone()
    
    conn.close()
    
    return dict(detection) if detection else None


# Initialize database on import
create_tables()
