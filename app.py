"""
Light Detection Web Application
Flask backend with MongoDB integration
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
import base64
from predict import LightDetector

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# MongoDB Configuration
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = 'light_detection'
COLLECTION_NAME = 'predictions'
CLIMATE_COLLECTION_NAME = 'climate_actions'

# Initialize MongoDB
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[DB_NAME]
    predictions_collection = db[COLLECTION_NAME]
    climate_collection = db[CLIMATE_COLLECTION_NAME]
    print(f"✓ Connected to MongoDB: {DB_NAME}")
except Exception as e:
    print(f"⚠ MongoDB connection error: {e}")
    print("  The app will run but data won't be saved.")
    predictions_collection = None
    climate_collection = None

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the light detector
MODEL_PATH = 'light_detection_model.h5'
detector = None

try:
    detector = LightDetector(MODEL_PATH)
    print(f"✓ Model loaded successfully: {MODEL_PATH}")
except Exception as e:
    print(f"⚠ Error loading model: {e}")
    print(f"  Please train the model first: python train_model.py")


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def save_prediction_to_db(filename, prediction_result, image_path):
    """Save prediction to MongoDB"""
    if predictions_collection is None:
        return None
    
    try:
        # Read image and convert to base64 for storage
        with open(image_path, 'rb') as img_file:
            image_data = base64.b64encode(img_file.read()).decode('utf-8')
        
        prediction_doc = {
            'filename': filename,
            'prediction': prediction_result['label'],
            'confidence': prediction_result['confidence'],
            'raw_score': prediction_result['raw_score'],
            'timestamp': datetime.utcnow(),
            'image_data': image_data  # Store image as base64
        }
        
        result = predictions_collection.insert_one(prediction_doc)
        return str(result.inserted_id)
    
    except Exception as e:
        print(f"Error saving to database: {e}")
        return None


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    if detector is None:
        return jsonify({
            'error': 'Model not loaded. Please train the model first.'
        }), 500
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check file type
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP, WEBP'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Make prediction
        result = detector.predict(filepath)
        
        if result is None:
            return jsonify({'error': 'Failed to process image'}), 500
        
        # Save to database
        db_id = save_prediction_to_db(filename, result, filepath)
        
        # Prepare response
        response = {
            'id': db_id,
            'filename': filename,
            'prediction': result['label'],
            'confidence': round(result['confidence'], 2),
            'raw_score': round(result['raw_score'], 4),
            'timestamp': datetime.now().isoformat(),
            'image_url': f'/uploads/{unique_filename}'
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get prediction history from MongoDB"""
    if predictions_collection is None:
        return jsonify([]), 200
    
    try:
        # Get limit parameter (default 50)
        limit = request.args.get('limit', 50, type=int)
        
        # Fetch predictions sorted by timestamp (newest first)
        predictions = predictions_collection.find(
            {},
            {'image_data': 0}  # Exclude image data for performance
        ).sort('timestamp', -1).limit(limit)
        
        # Convert to list and format
        history = []
        for pred in predictions:
            history.append({
                'id': str(pred['_id']),
                'filename': pred['filename'],
                'prediction': pred['prediction'],
                'confidence': round(pred['confidence'], 2),
                'raw_score': round(pred['raw_score'], 4),
                'timestamp': pred['timestamp'].isoformat()
            })
        
        return jsonify(history), 200
    
    except Exception as e:
        return jsonify({'error': f'Error fetching history: {str(e)}'}), 500


@app.route('/api/prediction/<prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    """Get a specific prediction with image"""
    if predictions_collection is None:
        return jsonify({'error': 'Database not available'}), 500
    
    try:
        prediction = predictions_collection.find_one({'_id': ObjectId(prediction_id)})
        
        if prediction is None:
            return jsonify({'error': 'Prediction not found'}), 404
        
        response = {
            'id': str(prediction['_id']),
            'filename': prediction['filename'],
            'prediction': prediction['prediction'],
            'confidence': round(prediction['confidence'], 2),
            'raw_score': round(prediction['raw_score'], 4),
            'timestamp': prediction['timestamp'].isoformat(),
            'image_data': prediction.get('image_data', '')
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': f'Error fetching prediction: {str(e)}'}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about predictions"""
    if predictions_collection is None:
        return jsonify({
            'total_predictions': 0,
            'lights_on_count': 0,
            'lights_off_count': 0,
            'average_confidence': 0
        }), 200
    
    try:
        total = predictions_collection.count_documents({})
        lights_on = predictions_collection.count_documents({'prediction': 'LIGHTS ON'})
        lights_off = predictions_collection.count_documents({'prediction': 'LIGHTS OFF'})
        
        # Calculate average confidence
        pipeline = [
            {'$group': {'_id': None, 'avg_confidence': {'$avg': '$confidence'}}}
        ]
        avg_result = list(predictions_collection.aggregate(pipeline))
        avg_confidence = round(avg_result[0]['avg_confidence'], 2) if avg_result else 0
        
        return jsonify({
            'total_predictions': total,
            'lights_on_count': lights_on,
            'lights_off_count': lights_off,
            'average_confidence': avg_confidence
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error fetching stats: {str(e)}'}), 500


@app.route('/api/clear-history', methods=['DELETE'])
def clear_history():
    """Clear all prediction history"""
    if predictions_collection is None:
        return jsonify({'error': 'Database not available'}), 500
    
    try:
        result = predictions_collection.delete_many({})
        return jsonify({
            'message': f'Deleted {result.deleted_count} predictions',
            'count': result.deleted_count
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error clearing history: {str(e)}'}), 500


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded images"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/api/save-climate-action', methods=['POST'])
def save_climate_action():
    """Save climate control action to MongoDB"""
    if climate_collection is None:
        return jsonify({'error': 'Database not available'}), 500
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['location', 'country', 'temperature', 'condition', 'heater_state', 'cooler_state']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create climate action document
        climate_doc = {
            'location': data['location'],
            'country': data['country'],
            'temperature': data['temperature'],
            'condition': data['condition'],
            'heater_state': data['heater_state'],
            'cooler_state': data['cooler_state'],
            'timestamp': datetime.utcnow()
        }
        
        result = climate_collection.insert_one(climate_doc)
        
        return jsonify({
            'message': 'Climate action saved successfully',
            'id': str(result.inserted_id)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error saving climate action: {str(e)}'}), 500


@app.route('/api/climate-history', methods=['GET'])
def get_climate_history():
    """Get climate control action history"""
    if climate_collection is None:
        return jsonify([]), 200
    
    try:
        # Get limit parameter (default 50)
        limit = request.args.get('limit', 50, type=int)
        
        # Fetch climate actions sorted by timestamp (newest first)
        actions = climate_collection.find().sort('timestamp', -1).limit(limit)
        
        # Convert to list and format
        history = []
        for action in actions:
            history.append({
                'id': str(action['_id']),
                'location': action['location'],
                'country': action['country'],
                'temperature': action['temperature'],
                'condition': action['condition'],
                'heater_state': action['heater_state'],
                'cooler_state': action['cooler_state'],
                'timestamp': action['timestamp'].isoformat()
            })
        
        return jsonify(history), 200
    
    except Exception as e:
        return jsonify({'error': f'Error fetching climate history: {str(e)}'}), 500


@app.route('/api/climate-stats', methods=['GET'])
def get_climate_stats():
    """Get statistics about climate control actions"""
    if climate_collection is None:
        return jsonify({
            'total_actions': 0,
            'heater_on_count': 0,
            'cooler_on_count': 0,
            'average_temperature': 0
        }), 200
    
    try:
        total = climate_collection.count_documents({})
        heater_on = climate_collection.count_documents({'heater_state': 'ON'})
        cooler_on = climate_collection.count_documents({'cooler_state': 'ON'})
        
        # Calculate average temperature
        pipeline = [
            {'$group': {'_id': None, 'avg_temp': {'$avg': '$temperature'}}}
        ]
        avg_result = list(climate_collection.aggregate(pipeline))
        avg_temp = round(avg_result[0]['avg_temp'], 2) if avg_result else 0
        
        return jsonify({
            'total_actions': total,
            'heater_on_count': heater_on,
            'cooler_on_count': cooler_on,
            'average_temperature': avg_temp
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error fetching climate stats: {str(e)}'}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'model_loaded': detector is not None,
        'database_connected': predictions_collection is not None
    }), 200


if __name__ == '__main__':
    print("\n" + "="*60)
    print("LIGHT DETECTION WEB APPLICATION")
    print("="*60)
    print(f"Model Status: {'✓ Loaded' if detector else '✗ Not loaded'}")
    print(f"Database Status: {'✓ Connected' if predictions_collection is not None else '✗ Not connected'}")
    print("="*60)
    print("\nStarting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
