from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader
import os

# Initialize the Flask app
app = Flask(__name__)

# Configure Cloudinary using environment variables
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Define a basic route to test if the server is running
@app.route('/')
def home():
    return "Flask is running with Gunicorn and using Railway's dynamic port!"

# Define the image processing route
@app.route('/process_image', methods=['POST'])
def process_image_request():
    try:
        data = request.json
        image_url = data.get('image_url')
        action = data.get('action')

        # Validate input
        if not image_url or not action:
            return jsonify({'status': 'error', 'message': 'Missing image_url or action'}), 400

        # Simulate image processing
        processed_image_url = cloudinary.uploader.upload(image_url)['url']

        return jsonify({
            'status': 'success',
            'processed_image_url': processed_image_url
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Start the server and bind to the correct host and port
if __name__ == '__main__':
    # Get the port from the environment (Railway provides it automatically)
    port = int(os.environ.get('PORT', 5000))  # Default to port 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)


