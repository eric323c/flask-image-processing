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
    # This will help you verify if the root route is working
    print("Home route accessed successfully.")
    return "Flask is running with Gunicorn!"

# Define the image processing route
@app.route('/process_image', methods=['POST'])
def process_image_request():
    try:
        # Log incoming request data for debugging purposes
        print("Processing image...")

        # Parse the incoming JSON payload
        data = request.json
        print(f"Received data: {data}")

        # Extract the image URL and action from the request
        image_url = data.get('image_url')
        action = data.get('action')

        # Check if both 'image_url' and 'action' are provided
        if not image_url or not action:
            print("Missing 'image_url' or 'action'.")
            return jsonify({'status': 'error', 'message': 'Missing image_url or action'}), 400

        # Log the extracted values
        print(f"Image URL: {image_url}, Action: {action}")

        # Simulate image processing logic (this is where your processing would go)
        processed_image_url = cloudinary.uploader.upload(image_url)['url']
        print(f"Processed image URL: {processed_image_url}")

        # Return a success response
        return jsonify({
            'status': 'success',
            'processed_image_url': processed_image_url
        })

    except Exception as e:
        # Log any errors that occur for debugging
        print(f"Error processing image: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


# This is only used when running the app locally; Gunicorn will handle serving the app in production
if __name__ == '__main__':
    # The app will listen on port 3000 in development mode
    # For production, this should be handled by Gunicorn, as Flask's built-in server is not recommended for production use
    app.run(host='0.0.0.0', port=3000)

