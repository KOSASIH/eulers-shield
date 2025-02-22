# api/app.py

from flask import Flask
from flask_cors import CORS
from routes import api_routes

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.register_blueprint(api_routes)  # Register API routes
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
