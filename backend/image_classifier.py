import os
import json
from datetime import datetime
import base64
from openai import OpenAI
from PIL import Image
import tempfile

class ImageClassifier:
    def __init__(self, api_key):
        """Initialize the ImageClassifier with OpenAI API key."""
        self.client = OpenAI(api_key=api_key)
        self.images_dir = tempfile.gettempdir()  # Use temp directory instead of classified_images
        self.analysis_file = os.path.join(self.images_dir, "image_analysis.json")
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories and files."""
        if not os.path.exists(self.analysis_file):
            with open(self.analysis_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def _encode_image(self, image_path):
        """Encode image to base64."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def save_uploaded_image(self, image_file):
        """Save uploaded image and return the filepath and base64 encoding."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{timestamp}.png"
        filepath = os.path.join(self.images_dir, filename)
        
        image = Image.open(image_file)
        image.save(filepath, 'PNG')
        
        # Get base64 encoding of the image
        encoded_image = self._encode_image(filepath)
        
        return filepath, encoded_image

    def analyze_image(self, image_path):
        """Analyze image using OpenAI Vision capabilities with merged analysis."""
        try:
            print("Analyzing image...")
            base64_image = self._encode_image(image_path)

            # Single request for complete analysis
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": """Analyze this image and provide a complete analysis in the following format:

# Image Classification Analysis

## 1. Classification Results
- Primary Category: [Main category] (Confidence: X%)
- Subcategories: [List relevant subcategories with confidence scores]

## 2. Subject Analysis
- Type: [Type of main subject] (Confidence: X%)
- Additional Classifications: [List if applicable]

## 3. Setting Analysis
- Environment: [Type] (Confidence: X%)
- Lighting: [Description] (Confidence: X%)
- Location Type: [Indoor/Outdoor] (Confidence: X%)

## 4. Technical Assessment
- Image Quality: [High/Medium/Low] (Confidence: X%)
- Color Scheme: [Description] (Confidence: X%)
- Composition: [Style description] (Confidence: X%)

## 5. Detailed Description

### Main Subject
- Physical Characteristics: [Description]
- Position/Arrangement: [Description]
- Notable Features: [Description]

### Environment Details
- Background Elements: [Description]
- Lighting Conditions: [Description]
- Spatial Context: [Description]

### Notable Elements
- Key Features: [Description]
- Unique Aspects: [Description]
- Points of Interest: [Description]

### Overall Impression
- Mood/Atmosphere: [Description]
- Intended Purpose: [Description]
- Key Takeaways: [Description]

Provide confidence scores (0-100%) where applicable and ensure descriptions are detailed and specific."""},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )

            # Compile analysis result with merged content
            analysis_result = {
                "classification": response.choices[0].message.content,
                "timestamp": datetime.now().isoformat(),
                "image_path": image_path,
                "image_data": base64_image  # Include base64 image data in result
            }

            # Save analysis
            self._save_analysis(image_path, analysis_result)
            return analysis_result

        except Exception as e:
            print(f"Error in image analysis: {e}")
            return None

    def _save_analysis(self, image_path, analysis):
        """Save analysis results to JSON file."""
        try:
            with open(self.analysis_file, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                filename = os.path.basename(image_path)
                data[filename] = analysis
                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.truncate()
        except Exception as e:
            print(f"Error saving analysis: {e}")

    def get_all_analyses(self):
        """Retrieve all image analyses."""
        try:
            with open(self.analysis_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading analyses: {e}")
            return {}