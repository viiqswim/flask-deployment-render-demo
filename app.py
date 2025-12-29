from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

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
        <h1>Welcome to Flask Demo App!</h1>
        <p>This is a simple Flask application ready for deployment on Render.</p>

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
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page with basic information"""
    return render_template_string(HOME_TEMPLATE)

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
        'app_name': 'Flask Demo App',
        'version': '1.0.0',
        'description': 'A simple Flask boilerplate for Render deployment'
    })

if __name__ == '__main__':
    # Render will use gunicorn, but this allows local development
    app.run(host='0.0.0.0', port=5000, debug=True)
