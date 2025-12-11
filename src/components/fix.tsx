from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS to allow requests from the React frontend running on localhost:3000
# This is crucial for local development to prevent 'Access-Control-Allow-Origin' errors.
# In a production environment, you would specify more restrictive origins or handle CORS via a proxy.
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api/message', methods=['GET'])
def get_message():
    """
    A simple API endpoint to test backend-frontend communication.
    Returns a JSON message.
    """
    return jsonify({
        "status": "success",
        "message": "Hello from the AI-Powered Code Review Backend!",
        "data": {
            "version": "1.0.0",
            "service": "CodeReviewAPI"
        }
    })

@app.route('/')
def health_check():
    """
    Basic health check endpoint.
    """
    return "Backend is running!"

if __name__ == '__main__':
    # Run the Flask app on port 5000 (default for Flask)
    # Ensure you have flask and flask-cors installed: pip install Flask Flask-CORS
    app.run(debug=True, port=5000)