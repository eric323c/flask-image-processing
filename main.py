from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader
import os

# Initialize Flask app
app = Flask(__name__)

# Configure Cloudinary with environment variables
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

@app.route('/')
def home():
    return "Image Processing API is running."

@app.route('/process_image', methods=['POST'])
def process_image_request():
    try:
        # Parse the incoming request
        data = request.json
        image_url = data.get('image_url')
        actions = data.get('actions')

        # Validate input
        if not image_url or not actions:
            return jsonify({'status': 'error', 'message': 'Missing image_url or actions'}), 400

        processed_image_url = image_url  # Start with the original image URL

        # Loop through the list of actions
        for action in actions:
            if action['action'] == 'crop':
                crop_options = {
                    "width": action.get('width', 100),
                    "height": action.get('height', 100),
                    "x": action.get('x', 50),
                    "y": action.get('y', 50)
                }
                processed_image_url = cloudinary.uploader.upload(processed_image_url, crop="crop", **crop_options)['url']
            elif action['action'] == 'grayscale':
                processed_image_url = cloudinary.uploader.upload(processed_image_url, effect="grayscale")['url']
            elif action['action'] == 'resize':
                resize_options = {
                    "width": action.get('width', 200),
                    "height": action.get('height', 200)
                }
                processed_image_url = cloudinary.uploader.upload(processed_image_url, width=resize_options["width"], height=resize_options["height"])['url']

        # Return the processed image URL
        return jsonify({
            'status': 'success',
            'processed_image_url': processed_image_url
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Railway's dynamic port or default to 5000
    app.run(host='0.0.0.0', port=port)
