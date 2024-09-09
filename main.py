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

@app.route('/')
def home():
    print("Home route accessed")
    return "Flask is running! Your image processing API is ready."

@app.route('/process_image', methods=['POST'])
def process_image_request():
    try:
        print("Processing image...")
        data = request.json
        image_url = data.get('image_url')
        action = data.get('action')
        print(f"Received image URL: {image_url}, Action: {action}")

        # Add more logic here and return response
        return jsonify({
            'status': 'success',
            'message': f'Processing {action} for image {image_url}'
        })
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
