from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

# Configure Cloudinary using environment variables
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Root route
@app.route('/')
def home():
    return "Flask is running! Your image processing API is ready."

# Image processing route (example route, you can extend this)
@app.route('/process_image', methods=['POST'])
def process_image_request():
    data = request.json
    image_url = data.get('image_url')
    action = data.get('action')

    # Simple response for now, replace with your logic
    return jsonify({
        'status': 'success',
        'message': f'Processing {action} for image {image_url}'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
