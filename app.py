import os
from flask import Flask, jsonify, render_template_string
from dotenv import load_dotenv

# Load environment variables from .env file for local development
# In production (Render), environment variables are set in the dashboard
load_dotenv()

app = Flask(__name__)

# Configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
app.config['ENV'] = os.getenv('ENVIRONMENT', 'production')

# Application settings from environment
APP_NAME = os.getenv('APP_NAME', 'Flask Demo App')
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
CUSTOM_MESSAGE = os.getenv('CUSTOM_MESSAGE', 'Welcome to our Flask application!')

# HTML template for the home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask Demo App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
        }
        .endpoint {
            background-color: #f0f0f0;
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to {{ app_name }}!</h1>
        <p>{{ custom_message }}</p>
        <p><strong>Environment:</strong> {{ environment }}</p>
        <p><strong>Version:</strong> {{ version }}</p>

        <h2>Available Endpoints:</h2>
        <div class="endpoint">
            <strong>GET /</strong> - This home page
        </div>
        <div class="endpoint">
            <strong>GET /api/health</strong> - <a href="/api/health">Health check endpoint</a>
        </div>
        <div class="endpoint">
            <strong>GET /api/info</strong> - <a href="/api/info">Application info</a>
        </div>
        <div class="endpoint">
            <strong>GET /api/config</strong> - <a href="/api/config">Configuration info</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page with basic information"""
    return render_template_string(
        HOME_TEMPLATE,
        app_name=APP_NAME,
        custom_message=CUSTOM_MESSAGE,
        environment=ENVIRONMENT,
        version=APP_VERSION
    )

@app.route('/api/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running'
    })

@app.route('/api/info')
def info():
    """Application information endpoint"""
    return jsonify({
        'app_name': APP_NAME,
        'version': APP_VERSION,
        'environment': ENVIRONMENT,
        'description': 'A simple Flask boilerplate for Render deployment with environment variables'
    })

@app.route('/api/config')
def config():
    """Configuration endpoint - shows environment-based settings"""
    return jsonify({
        'app_name': APP_NAME,
        'version': APP_VERSION,
        'environment': ENVIRONMENT,
        'debug': app.config['DEBUG'],
        'custom_message': CUSTOM_MESSAGE,
        'flask_env': app.config['ENV']
    })

if __name__ == '__main__':
    # Render will use gunicorn, but this allows local development
    app.run(host='0.0.0.0', port=5000, debug=True)
