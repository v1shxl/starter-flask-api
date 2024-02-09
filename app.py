from flask import Flask, request, jsonify
import base64
import cv2
from PIL import Image
import numpy as np

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Receive base64 encoded image from Flutter app
        data = request.get_json()
        encoded_image = data['image']
        
        # Decode base64 encoded image
        decoded_image = base64.b64decode(encoded_image)
        
        # Convert bytes to numpy array
        nparr = np.frombuffer(decoded_image, np.uint8)
        
        # Decode numpy array to OpenCV image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Process the image (e.g., object detection with YOLO)
        # For demonstration, we'll simply convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Encode processed image to base64
        _, encoded_processed_image = cv2.imencode('.png', gray_image)
        base64_processed_image = base64.b64encode(encoded_processed_image).decode('utf-8')
        
        return jsonify({'processed_image': base64_processed_image})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
