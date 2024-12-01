# main.py
import os
import json
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from backend.image_classifier import ImageClassifier
import webview

# Initialize Flask app
app = Flask(__name__, static_folder='frontend/dist')
CORS(app)

# Add your OpenAI API key here
API_KEY = "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"

# Create necessary directories
os.makedirs('classified_images', exist_ok=True)

@app.route('/')
def serve_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), path)

@app.route('/api/classify-image', methods=['POST'])
def classify_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        classifier = ImageClassifier(API_KEY)
        filepath = classifier.save_uploaded_image(file)
        analysis = classifier.analyze_image(filepath)
        
        if analysis:
            return jsonify(analysis)
        return jsonify({'error': 'Analysis failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/image-analyses')
def get_image_analyses():
    try:
        classifier = ImageClassifier(API_KEY)
        return jsonify(classifier.get_all_analyses())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/classified_images/<path:filename>')
def serve_classified_image(filename):
    return send_from_directory('classified_images', filename)

if __name__ == '__main__':
    # Create empty analysis file if it doesn't exist
    if not os.path.exists('classified_images/image_analysis.json'):
        with open('classified_images/image_analysis.json', 'w') as f:
            json.dump({}, f)
    
    app.run(port=5000, debug=True)