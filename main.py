# main.py
import os
import json
import tempfile
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from backend.image_classifier import ImageClassifier
from dotenv import load_dotenv

load_dotenv() 

# Initialize Flask app
app = Flask(__name__, static_folder='frontend/dist')
# Update CORS to allow requests from your Vercel frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://image-insight-n81u2h8gq-athrvaaroras-projects.vercel.app",
            "https://image-insight-clib88dp0-athrvaaroras-projects.vercel.app",
            "https://image-insight-ce8atzsvm-athrvaaroras-projects.vercel.app"
            "https://image-classification-gcp.vercel.app
"    
            "http://localhost:5000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "expose_headers": ["Content-Type"],
        "support_credentials": True
    }
})

# Add your OpenAI API key here
API_KEY = os.getenv('OPENAI_API_KEY')

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
        filepath, encoded_image = classifier.save_uploaded_image(file)
        analysis = classifier.analyze_image(filepath)
        
        if analysis:
            # Make sure analysis contains the base64 image data
            if 'image_data' not in analysis:
                analysis['image_data'] = encoded_image
            return jsonify(analysis)
        return jsonify({'error': 'Analysis failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/image-analyses')
def get_image_analyses():
    try:
        classifier = ImageClassifier(API_KEY)
        analyses = classifier.get_all_analyses()
        return jsonify(analyses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)